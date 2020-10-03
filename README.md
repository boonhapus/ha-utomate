# Hautomate [[Home Assistant][hass] Component]

A task automation library focused on home automation.

Visit the [Wiki][wiki] for more information.

---

### Looking for the hautomate library documentation?
#### 👉 [click here][hauto] 👈


## Getting Started

The best way to get up and running with `hautomate` in HomeAssistant is with [HACS][hacs] as a [custom repository][hacs-custrepo].

All that's left to do is add hautomate to your `configuration.yaml` with a directive pointing to the directory that holds all your Apps!

```yaml
hautomate:
  apps_dir: /path/to/my/apps/
```

Optionally, if you'd like to just test if your install is working, you may use the constant `hello_world`.
```yaml
hautomate:
  apps_dir: hello_world
```

<p align="center">
    <img src="./static/ui-example.png" alt='ui-example'>
</p>

[hass]: https://www.home-assistant.io/
[wiki]: https://github.com/boonhapus/ha-utomate/wiki
[hauto]: https://github.com/boonhapus/hautomate
[hacs]: https://hacs.xyz/
[hacs-custrepo]: https://hacs.xyz/docs/faq/custom_repositories
[ui-eg]: ./static/ui-example.png
