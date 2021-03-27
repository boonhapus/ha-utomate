
# Hautomate

A task automation library focused on home automation.


### Recent Changelog

**[\[v0.2.0\]][0.2.0]** - 🕷 Sensors, Wrap up work, Infinite Loop Bug!
`+` ability to create Sensors in HomeAssistant
`+` teardown logic to cleanup user-created Switches and Sensors
`*` disambiguate Intent entities with entity_id prefix of 'hauto_'
`*` fixed infinite loop with some event triggers
`-` minor hygiene and typo cleanup

**[\[v0.1.1\]][0.1.1]** - 🧹 Just tidying up around here..
`+` minor code documentation, README, INFO
`+` `hello_world.HelloWorld` App: a way for you to test your install!
`+` `hassfest.yaml` to ensure we're actually in working order
`-` cleanup of MVP artifacts

**[\[v0.1.0\]][0.1.0]** - 🎉 Functional MVP! Connected hauto to hass.
*The hautomate custom component provides..*
`+` bidirectional connection between the hautomate and Home Assistant event busses
`+` hauto Intents visible inside the hass frontend as a toggleable switch
`+` hauto Intents communicate data to hass immediately
`+` hass Intent Switch can be paused or readied from the front end

[0.1.0]: https://github.com/boonhapus/ha-utomate/releases/tag/v0.1.0
[0.1.1]: https://github.com/boonhapus/ha-utomate/releases/tag/v0.1.1
[0.2.0]: https://github.com/boonhapus/ha-utomate/releases/tag/v0.2.0
