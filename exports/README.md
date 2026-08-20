# Luna bronexport

Deze map bevat de geschoonde configuratielogica die rechtstreeks uit de actuele Luna-Test Home Assistant-configuratie is gelezen.

## Inventaris

- Automatiseringen gelezen: 91 (core 13, test 78)
- Helpers gelezen: 381 (op GitHub gezet 363, uitgesloten 18)
- Scripts gelezen: 8 (core 4, test 4)

De YAML-bestanden zijn JSON-vormige YAML-lijsten. Ze zijn bedoeld als bronexport/reference en niet als blind importbestand: echte apparaten, meldingen, gebruikers, locaties, netwerkadressen, gebruikers-ID's en geheugenwaarden zijn vervangen door placeholders of verwijderd. Fysieke acties blijven daardoor fail-closed totdat een klant ze expliciet configureert.

Testlogica staat uitsluitend in de bestanden met `luna_test_` of `luna_test.yaml`. De standaard klantpakketten staan onder `packages/`.

## Privacyfilter

Uitgesloten: personen en gebruikers-ID's, echte telefoons en meldkanalen, kamer- en apparaatnamen, IP/MAC-adressen, URL's, wachtwoorden/tokens, gesprekken en persoonlijke geheugenrecords. Geheugen- en tellerinitialen zijn leeg of nul gemaakt.
