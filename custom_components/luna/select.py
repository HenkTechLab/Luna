"""Native Home Assistant select entities for Luna setup."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_CALENDAR_ENTITY,
    CONF_CONTROL_ENTITIES,
    CONF_ENERGY_ENTITY,
    CONF_OBSERVATION_ENTITIES,
    CONF_POWER_ENTITY,
    CONF_PRESENCE_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    DOMAIN,
    SOURCE_OPTION_KEYS,
)

UNSET = "Niet ingesteld"
CHOOSE = "Kies een entiteit…"
NONE_SELECTED = "Geen gekoppelde entiteiten"

CONTROL_DOMAINS = {
    "light",
    "switch",
    "cover",
    "climate",
    "fan",
    "lock",
    "media_player",
}
PRESENCE_DOMAINS = {"binary_sensor", "person", "device_tracker", "input_boolean"}
OBSERVATION_DOMAINS = {"sensor", "binary_sensor"}


@dataclass(frozen=True, kw_only=True)
class LunaCoreSelectDescription:
    """Describe one native Luna source selector."""

    option_key: str
    name: str
    object_id: str
    icon: str
    kind: str


CORE_SELECTS = (
    LunaCoreSelectDescription(
        option_key=CONF_PRESENCE_ENTITY,
        name="Aanwezigheid",
        object_id="luna_aanwezigheidsbron",
        icon="mdi:home-account",
        kind="presence",
    ),
    LunaCoreSelectDescription(
        option_key=CONF_TEMPERATURE_ENTITY,
        name="Hoofdtemperatuur",
        object_id="luna_temperatuurbron",
        icon="mdi:thermometer",
        kind="temperature",
    ),
    LunaCoreSelectDescription(
        option_key=CONF_ENERGY_ENTITY,
        name="Energie",
        object_id="luna_energiebron",
        icon="mdi:lightning-bolt",
        kind="energy",
    ),
    LunaCoreSelectDescription(
        option_key=CONF_POWER_ENTITY,
        name="Vermogen",
        object_id="luna_vermogenbron",
        icon="mdi:flash",
        kind="power",
    ),
    LunaCoreSelectDescription(
        option_key=CONF_CALENDAR_ENTITY,
        name="Agenda",
        object_id="luna_agendabron",
        icon="mdi:calendar",
        kind="calendar",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Luna's native setup selectors."""
    entities: list[SelectEntity] = [
        LunaCoreSourceSelect(hass, entry, description)
        for description in CORE_SELECTS
    ]
    entities.extend(
        [
            LunaListMutationSelect(
                hass,
                entry,
                mapping_key=CONF_OBSERVATION_ENTITIES,
                mode="add",
                name="Extra observatie toevoegen",
                object_id="luna_observatie_toevoegen",
                icon="mdi:database-plus",
            ),
            LunaListMutationSelect(
                hass,
                entry,
                mapping_key=CONF_OBSERVATION_ENTITIES,
                mode="remove",
                name="Extra observatie verwijderen",
                object_id="luna_observatie_verwijderen",
                icon="mdi:database-minus",
            ),
            LunaListMutationSelect(
                hass,
                entry,
                mapping_key=CONF_CONTROL_ENTITIES,
                mode="add",
                name="Apparaat toevoegen",
                object_id="luna_apparaat_toevoegen",
                icon="mdi:plus-circle-outline",
            ),
            LunaListMutationSelect(
                hass,
                entry,
                mapping_key=CONF_CONTROL_ENTITIES,
                mode="remove",
                name="Apparaat verwijderen",
                object_id="luna_apparaat_verwijderen",
                icon="mdi:minus-circle-outline",
            ),
        ]
    )
    async_add_entities(entities)


def _device_info(entry: ConfigEntry) -> DeviceInfo:
    """Return Luna device metadata."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Luna",
        manufacturer="HenkTechLab",
        model="Luna sensor bridge",
    )


def _display_name(state: State) -> str:
    """Return a unique, user-friendly selector option."""
    friendly_name = state.attributes.get("friendly_name", state.entity_id)
    return f"{friendly_name} ({state.entity_id})"


def _matches_kind(state: State, kind: str) -> bool:
    """Return whether a Home Assistant state is valid for a Luna source kind."""
    domain = state.entity_id.split(".", 1)[0]
    device_class = state.attributes.get("device_class")

    if kind == "presence":
        return domain in PRESENCE_DOMAINS
    if kind == "temperature":
        return domain == "sensor" and device_class == "temperature"
    if kind == "energy":
        return domain == "sensor" and device_class == "energy"
    if kind == "power":
        return domain == "sensor" and device_class == "power"
    if kind == "calendar":
        return domain == "calendar"
    if kind == "observation":
        return domain in OBSERVATION_DOMAINS and not state.entity_id.startswith(
            ("sensor.luna_", "binary_sensor.luna_")
        )
    if kind == "control":
        return domain in CONTROL_DOMAINS
    return False


def _candidate_map(
    hass: HomeAssistant,
    kind: str,
    *,
    excluded: set[str] | None = None,
    only: set[str] | None = None,
) -> dict[str, str]:
    """Build display-label to entity-id mapping for a native selector."""
    excluded = excluded or set()
    candidates: list[State] = []

    for state in hass.states.async_all():
        if state.entity_id in excluded:
            continue
        if only is not None and state.entity_id not in only:
            continue
        if _matches_kind(state, kind):
            candidates.append(state)

    candidates.sort(
        key=lambda state: (
            str(state.attributes.get("friendly_name", state.entity_id)).casefold(),
            state.entity_id,
        )
    )
    return {_display_name(state): state.entity_id for state in candidates}


class LunaCoreSourceSelect(SelectEntity):
    """Select one primary Luna source directly from the dashboard."""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: LunaCoreSelectDescription,
    ) -> None:
        """Initialize the source selector."""
        self._hass = hass
        self._entry = entry
        self._description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.option_key}_select"
        self._attr_name = description.name
        self._attr_suggested_object_id = description.object_id
        self._attr_icon = description.icon
        self._attr_device_info = _device_info(entry)

    @property
    def _mapping(self) -> dict[str, str]:
        mapping = _candidate_map(self._hass, self._description.kind)
        current = self._entry.options.get(self._description.option_key)
        if current and current not in mapping.values():
            state = self._hass.states.get(current)
            label = _display_name(state) if state is not None else current
            mapping[label] = current
        return mapping

    @property
    def options(self) -> list[str]:
        """Return selectable Home Assistant entities."""
        return [UNSET, *self._mapping.keys()]

    @property
    def current_option(self) -> str:
        """Return the currently configured source."""
        current = self._entry.options.get(self._description.option_key)
        if not current:
            return UNSET
        for label, entity_id in self._mapping.items():
            if entity_id == current:
                return label
        return UNSET

    async def async_select_option(self, option: str) -> None:
        """Persist the selected source using the config entry's normal options."""
        new_options = dict(self._entry.options)
        if option == UNSET:
            new_options.pop(self._description.option_key, None)
        else:
            entity_id = self._mapping.get(option)
            if entity_id is None:
                return
            new_options[self._description.option_key] = entity_id

            observations = list(
                new_options.get(CONF_OBSERVATION_ENTITIES, [])
            )
            if entity_id in observations:
                observations.remove(entity_id)
                new_options[CONF_OBSERVATION_ENTITIES] = observations

        if new_options == dict(self._entry.options):
            return

        self._hass.config_entries.async_update_entry(
            self._entry, options=new_options
        )
        self._hass.async_create_task(
            self._hass.config_entries.async_reload(self._entry.entry_id)
        )


class LunaListMutationSelect(SelectEntity):
    """Add or remove one item from a multi-entity Luna mapping."""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        *,
        mapping_key: str,
        mode: str,
        name: str,
        object_id: str,
        icon: str,
    ) -> None:
        """Initialize an add/remove selector."""
        self._hass = hass
        self._entry = entry
        self._mapping_key = mapping_key
        self._mode = mode
        self._attr_unique_id = f"{entry.entry_id}_{object_id}"
        self._attr_name = name
        self._attr_suggested_object_id = object_id
        self._attr_icon = icon
        self._attr_device_info = _device_info(entry)

    @property
    def _configured(self) -> list[str]:
        return list(self._entry.options.get(self._mapping_key, []))

    @property
    def _mapping(self) -> dict[str, str]:
        kind = (
            "observation"
            if self._mapping_key == CONF_OBSERVATION_ENTITIES
            else "control"
        )
        configured = set(self._configured)

        if self._mode == "remove":
            mapping = _candidate_map(
                self._hass, kind, only=configured
            )
            missing = configured - set(mapping.values())
            for entity_id in sorted(missing):
                mapping[entity_id] = entity_id
            return mapping

        excluded = configured
        if self._mapping_key == CONF_OBSERVATION_ENTITIES:
            excluded = excluded | {
                entity_id
                for key in SOURCE_OPTION_KEYS
                if (entity_id := self._entry.options.get(key))
            }
        return _candidate_map(self._hass, kind, excluded=excluded)

    @property
    def options(self) -> list[str]:
        """Return addable or removable entities."""
        mapping = self._mapping
        if not mapping:
            return [NONE_SELECTED if self._mode == "remove" else CHOOSE]
        return [CHOOSE, *mapping.keys()]

    @property
    def current_option(self) -> str:
        """Keep the selector in an action-ready neutral state."""
        if self._mode == "remove" and not self._mapping:
            return NONE_SELECTED
        return CHOOSE

    async def async_select_option(self, option: str) -> None:
        """Add or remove the chosen entity and immediately persist it."""
        if option in {CHOOSE, NONE_SELECTED}:
            return

        entity_id = self._mapping.get(option)
        if entity_id is None:
            return

        configured = self._configured
        if self._mode == "add":
            if entity_id in configured:
                return
            configured.append(entity_id)
        else:
            if entity_id not in configured:
                return
            configured.remove(entity_id)

        new_options = dict(self._entry.options)
        new_options[self._mapping_key] = configured
        self._hass.config_entries.async_update_entry(
            self._entry, options=new_options
        )
        self._hass.async_create_task(
            self._hass.config_entries.async_reload(self._entry.entry_id)
        )
