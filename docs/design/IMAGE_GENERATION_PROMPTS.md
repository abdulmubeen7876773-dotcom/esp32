# ESP32 Engine Image Generation Prompts

## Purpose

This document defines reusable prompts for generating consistent ESP32 Engine project artwork later. Do not generate images from this file automatically. These prompts are production briefs for future use with ChatGPT image generation, DALL-E, or a similar visual tool.

All generated project images should look like the same premium electronics learning platform.

## Master Style Prompt

Use this base prompt before each project-specific prompt:

```text
Premium educational electronics photography for ESP32 Engine. A real ESP32 development board is clearly visible in a finished working project on a clean modern lab workbench. Soft diffused top-left lighting, subtle cool blue rim light, realistic shadows, clean matte graphite or soft white surface, faint PCB trace motif in the background, modern engineering aesthetic, practical and trustworthy, Apple and Stripe level polish, no clutter, no hands, no random stock-photo props, no text overlays, no watermarks, no logos other than realistic markings on electronics, consistent cool color grading with small warm LED highlights, shallow but readable depth of field, 16:9 composition, high detail, realistic hardware.
```

## Negative Prompt

Use this with every project:

```text
Avoid cartoon style, toy-like electronics, messy wires, dark gaming neon, cyberpunk lighting, fantasy circuit backgrounds, fake floating holograms, random stock laptop scenes, unreadable components, invisible ESP32 board, hands, people, brand logos, watermark, text overlay, excessive blur, excessive glow, low-resolution artifacts, duplicated wires, impossible wiring, unsafe mains wiring, cluttered desk.
```

## Camera Standard

Use this camera direction unless a project calls for a different view:

```text
Camera angle: 3/4 top-down view from the front-right, about 40 degrees above the workbench, 50mm to 70mm lens feel, project centered with the ESP32 in the central or lower central third, primary sensor or output visible in the upper third, 8 percent safe area on all sides for responsive cropping.
```

## Priority Top 10 Project Prompts

These are the first ten project artwork briefs to produce so homepage, project cards, and social previews can share one visual direction.

### 1. ESP32 Mini Weather Station

Asset target: `assets/visuals/projects/heroes/esp32-iot-weather-station-hero.webp`

Camera angle: 3/4 top-down, ESP32 and DHT22 on breadboard in foreground, small OLED or serial-style display module visible behind it.

Lighting: Soft top-left key light, cool blue rim behind the ESP32, tiny teal display glow.

Background: Matte graphite workbench with faint PCB traces, clean cable routing, no extra tools.

Composition: ESP32 lower center, DHT22 sensor to the right, display reading temperature and humidity in the upper third.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 mini weather station on a clean matte graphite lab workbench, ESP32 DevKit clearly visible on a breadboard, DHT22 temperature and humidity sensor connected with tidy red, black, and blue jumper wires, small OLED display showing simple temperature and humidity values without readable brand text, USB cable neatly routed, subtle cool blue rim light behind the board, soft diffused top-left lighting, faint PCB trace motif in the background, realistic shadows, practical beginner-friendly project, clean modern engineering aesthetic, 16:9 composition.
```

### 2. ESP32 Smart Thermostat

Asset target: `assets/visuals/projects/heroes/esp32-smart-thermostat-hero.webp`

Camera angle: 3/4 top-down, thermostat display or enclosure in upper third, ESP32 and relay visible below.

Lighting: Soft white key light with subtle blue ambient edge; small warm indicator LED allowed.

Background: Soft white or light gray bench, premium home-lab feel.

Composition: ESP32 lower center, DHT22 sensor and relay module clearly separated, thermostat display as the visible result.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 smart thermostat project on a clean soft white lab workbench, ESP32 DevKit clearly visible, DHT22 sensor, single-channel relay module, and a small display or compact thermostat-style enclosure showing a simple temperature value, tidy jumper wires with safe low-voltage bench setup, no mains wiring visible, soft diffused top-left lighting, subtle cool blue rim light, realistic shadows, premium modern home automation learning project, clean and trustworthy, 16:9 composition.
```

### 3. ESP32 Line Following Robot

Asset target: `assets/visuals/projects/heroes/esp32-line-following-robot-hero.webp`

Camera angle: Low 3/4 top-down, robot angled along a black tape line.

Lighting: Soft overhead key with cool rim on chassis edges.

Background: Clean matte surface with a simple black line track.

Composition: Robot fills the center, ESP32 visible on top, IR sensor array visible at the front.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 line following robot on a clean matte light-gray test surface with a black tape track, two-wheel robot chassis, ESP32 DevKit clearly mounted on top, IR sensor array visible at the front, motor driver and battery pack arranged cleanly, tidy wiring, robot angled as if ready to follow the line, soft diffused top-left lighting, subtle cool blue rim light, realistic engineering classroom feel, no clutter, 16:9 composition.
```

### 4. ESP32 Smart Irrigation System

Asset target: `assets/visuals/projects/heroes/esp32-smart-irrigation-system-hero.webp`

Camera angle: 3/4 top-down, small planter and electronics on same clean surface.

Lighting: Soft daylight-style key, gentle teal accent near sensor/readout.

Background: Matte graphite bench with one small plant container, not a garden stock photo.

Composition: ESP32 and relay lower center, soil moisture probe inserted into planter at upper right, tubing or small pump visible but tidy.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 smart irrigation system on a clean modern lab workbench, ESP32 DevKit clearly visible on a breadboard, capacitive soil moisture sensor inserted into a small minimal planter, relay module and small low-voltage pump or water tube arranged neatly, tidy red, black, and signal jumper wires, subtle teal sensor accent, soft diffused top-left lighting, cool blue rim light, faint PCB trace motif in the background, practical agriculture learning project, 16:9 composition.
```

### 5. ESP32 Motion Security Alert

Asset target: `assets/visuals/projects/heroes/esp32-motion-security-alert-hero.webp`

Camera angle: 3/4 top-down, PIR sensor facing camera, ESP32 visible behind it.

Lighting: Soft key with restrained red alert LED highlight.

Background: Deep navy or graphite bench, subtle security feel without drama.

Composition: PIR sensor in foreground, ESP32 and buzzer/LED arranged cleanly, optional doorway mockup blurred in background.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 motion security alert project on a clean matte graphite workbench, ESP32 DevKit clearly visible, HC-SR501 PIR motion sensor facing forward, small buzzer and red indicator LED connected with tidy jumper wires, no people, optional minimal doorway model softly blurred in the background, soft diffused top-left lighting, subtle cool blue rim light, tiny restrained red alert glow, professional security electronics learning project, 16:9 composition.
```

### 6. ESP32 Camera Capture Server

Asset target: `assets/visuals/projects/heroes/esp32-camera-capture-server-hero.webp`

Camera angle: 3/4 top-down with ESP32-CAM module on small stand, laptop/browser blurred in background only if needed.

Lighting: Soft top-left key, blue rim around camera module.

Background: Clean matte graphite surface with a neutral object in camera view.

Composition: ESP32-CAM upper center, USB adapter or power module visible, browser preview softly out of focus in background.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 camera capture server project on a clean modern lab workbench, ESP32-CAM module clearly visible on a small simple stand, camera lens facing a small neutral test object, USB serial adapter or power connection arranged neatly, optional laptop in the far background showing a softly blurred image preview with no readable text, soft diffused top-left lighting, subtle cool blue rim light, realistic shadows, clean ESP32-CAM learning project, 16:9 composition.
```

### 7. ESP32 Air Quality Monitor

Asset target: `assets/visuals/projects/heroes/esp32-air-quality-monitor-hero.webp`

Camera angle: 3/4 top-down, gas sensor and display visible with ESP32.

Lighting: Soft white key, teal display glow, minimal amber sensor warmth if realistic.

Background: Light gray lab bench with subtle air-flow visual implied by composition, not smoke.

Composition: ESP32 lower center, gas sensor module and small fan or OLED upper area.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 air quality monitor on a clean light-gray lab workbench, ESP32 DevKit clearly visible, gas sensor module and small OLED display connected with tidy jumper wires, optional small low-voltage fan module placed neatly beside the sensor, display suggests air quality status without prominent readable overlay text, soft diffused top-left lighting, subtle teal and blue electronic glow, realistic shadows, clean environmental monitoring project, 16:9 composition.
```

### 8. ESP32 WiFi Robot Controller

Asset target: `assets/visuals/projects/heroes/esp32-wifi-robot-controller-hero.webp`

Camera angle: 3/4 top-down, robot angled toward viewer, controller phone blurred in background.

Lighting: Soft key with blue network accent.

Background: Matte graphite surface, faint PCB traces.

Composition: ESP32 robot car centered, motor driver and wheels visible, phone UI blurred enough to avoid readable text.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 WiFi robot controller project on a clean matte graphite workbench, compact two-wheel robot chassis with ESP32 DevKit clearly visible on top, motor driver and battery pack arranged cleanly, tidy wiring, smartphone controller placed softly out of focus in the background with no readable interface text, subtle blue Wi-Fi inspired accent light, soft diffused top-left lighting, realistic shadows, modern robotics learning project, 16:9 composition.
```

### 9. ESP32 Smart Door Lock

Asset target: `assets/visuals/projects/heroes/esp32-smart-door-lock-hero.webp`

Camera angle: 3/4 top-down, small door mockup with keypad/servo lock and ESP32 visible.

Lighting: Soft white key with restrained blue rim.

Background: Clean workbench with a minimal wooden or acrylic door model.

Composition: ESP32 lower center, keypad and servo lock on upper half, wires tidy and readable.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 smart door lock project on a clean modern lab workbench, small minimal door mockup with keypad and servo lock mechanism, ESP32 DevKit clearly visible beside it, tidy jumper wires connecting keypad and servo, safe low-voltage educational setup, soft diffused top-left lighting, subtle cool blue rim light, realistic shadows, premium home automation learning project, no clutter, 16:9 composition.
```

### 10. ESP32 MQTT Sensor Dashboard

Asset target: `assets/visuals/projects/heroes/esp32-mqtt-sensor-dashboard-hero.webp`

Camera angle: 3/4 top-down, sensor node in foreground and blurred dashboard screen behind.

Lighting: Soft key, cool blue network glow.

Background: Matte graphite desk with faint PCB trace motif.

Composition: ESP32 and sensor node lower center, laptop or tablet dashboard blurred in upper third with chart-like blocks but no readable text.

Prompt:

```text
Premium educational electronics photography for ESP32 Engine. Finished ESP32 MQTT sensor dashboard project on a clean matte graphite workbench, ESP32 DevKit clearly visible with temperature and humidity sensor connected neatly, small OLED or status LED optional, laptop or tablet in the background showing a softly blurred dashboard with simple chart shapes and no readable text, subtle blue network glow, soft diffused top-left lighting, realistic shadows, modern IoT learning platform feel, faint PCB trace motif, 16:9 composition.
```

## Thumbnail Crop Directions

After generating a project hero, create the thumbnail from the same scene:

```text
Crop to 8:5. Keep the ESP32 board, main component, and visible output inside the crop. Preserve at least 10 percent safe area. Increase local contrast slightly for card readability. Do not add text overlays.
```

## Open Graph Direction

For project OG images, reuse the project hero scene and compose a cover:

```text
Create a 1200 x 630 Open Graph image for ESP32 Engine. Use the generated project hardware scene on the right side, deep navy or soft blue premium background, subtle PCB traces, ESP32 Engine logo in the top-left safe area, project title on the left with strong readable contrast, small category label, no long description, no clutter, no watermark.
```

## Review Checklist

Before accepting generated artwork:

- ESP32 board is visible and realistic.
- The main sensor, actuator, display, or module is visible.
- Wiring looks tidy and plausible.
- Lighting matches the master style.
- Background is clean and premium.
- No random stock-photo objects were introduced.
- No text overlays or watermarks are present.
- The image works at 16:9 hero size and 8:5 thumbnail crop.
- The image feels educational, not promotional or flashy.
