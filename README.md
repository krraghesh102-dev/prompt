# DEAD ZONE — Zombie Wave Shooter

A top-down zombie survival shooter. Endless waves, three weapons, score chasing.
Single HTML file, no build step, no dependencies, no assets.

## Play

Open `index.html` in any modern browser. That's it.

## Controls

| Input | Action |
|---|---|
| `WASD` / arrow keys | Move |
| Mouse | Aim |
| Left click / hold | Shoot |
| `Shift` | Sprint (drains stamina) |
| `R` | Reload |
| `1` `2` `3` | Switch weapon |
| `P` / `Esc` | Pause |

Touch: left half of the screen is a virtual move stick, right half aims and fires.

## How it plays

Zombies spawn off-screen and close in from every edge. Clear the wave, get a
short breather plus a bonus, then the next wave starts — bigger, faster, tougher.
Each wave scales enemy count, health, and speed, and mixes in nastier types.

**Enemies**

- **Walker** — slow, common, 10 pts
- **Runner** — fast and fragile, from wave 2, 18 pts
- **Brute** — heavy, high HP, big damage, from wave 5, 45 pts
- **Spitter** — keeps its distance and lobs acid, from wave 7, 30 pts

**Weapons** — the shotgun unlocks at wave 3, the rifle at wave 6.

- **Pistol** — semi-auto, accurate, unlimited reserve ammo
- **Shotgun** — 7 pellets, heavy knockback, short range
- **Rifle** — full-auto, high fire rate, burns through ammo

**Scoring** — kills award points, and a kill streak builds a combo multiplier
(up to 2.5x) that decays if you stop killing. Clearing a wave pays a bonus
scaled by wave number and remaining health. Best score persists in
`localStorage`.

**Drops** — dead zombies sometimes leave medkits (+25 HP) or ammo boxes.

## Structure

Everything lives in `index.html`: markup, CSS, and the game in a single
`<script>`. The game is a fixed 960x600 logical canvas scaled to fit the
window, with a `requestAnimationFrame` loop, delta-time normalized to 60fps,
and a small WebAudio synth for sound (no audio files).
