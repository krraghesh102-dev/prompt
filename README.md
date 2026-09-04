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
| `G` | Throw grenade |
| `F` | Raise security layer (shield) |
| `Q` | Power blast |
| `P` / `Esc` | Pause |

## On a phone

Play it in **landscape** — the game shows a rotate prompt and pauses in portrait.

Twin-stick controls. Both sticks **float**: they appear wherever your thumb
lands, so there is no fixed pad to hunt for.

| Touch | Action |
|---|---|
| **Left half** — drag anywhere | Move in any direction; push far to sprint |
| **Right half** — drag anywhere | Aim in that direction and fire continuously |
| **Right half** — quick tap | Fire at the exact spot you tapped |
| On-screen buttons (top-left) | Weapon slots, reload, pause |
| On-screen buttons (bottom-right) | Grenade, shield, power blast |

Both thumbs work at once, so you can retreat while firing behind you.

Because aim on the right stick is a *direction* rather than a screen
position, every heading is reachable — including straight back over the
hand that is moving you. The playfield width follows the screen aspect
ratio, so the game fills a phone edge to edge.

## How it plays

Zombies spawn off-screen and close in from every edge. Clear the wave, get a
short breather plus a bonus, then the next wave starts — bigger, faster, tougher.
Each wave scales enemy count, health, and speed, and mixes in nastier types.

**Enemies**

- **Walker** — slow, common, 10 pts
- **Runner** — fast and fragile, from wave 2, 18 pts
- **Brute** — heavy, high HP, big damage, from wave 5, 45 pts
- **Spitter** — keeps its distance and lobs acid, from wave 7, 30 pts

**Armory** — three guns, plus three limited-charge items.

*Guns* — the shotgun unlocks at wave 3, the rifle at wave 6.

- **Pistol** — semi-auto, accurate, unlimited reserve ammo
- **Shotgun** — 7 pellets, heavy knockback, short range
- **Rifle** — full-auto, high fire rate, burns through ammo

*Gear* — each has limited charges, shown bottom-right. Charges drop from
kills and top up between waves (a grenade every wave, a shield every third,
a blast every fourth).

- **Grenade** (`G`) — thrown along your aim, ~0.8s fuse, bounces off walls.
  118px blast with damage falling off to the rim. It **will hurt you** at
  half damage if you are inside the radius, so mind the bounce.
- **Security layer** (`F`) — a full-body barrier that absorbs *all* damage
  for 6.5 seconds, bites and acid included. A ring around you counts the
  time down. Using it while already up extends the timer rather than
  restarting it, so a charge is never wasted.
- **Power blast** (`Q`) — an instant 210px shockwave centered on you.
  Heavy damage with falloff plus a hard shove outward, and it never hurts
  you. Clears a surrounding pack of walkers outright. Short cooldown so one
  press spends exactly one charge.

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

The world height is fixed at 600 so enemy and player scale stay constant;
the width is recomputed from the viewport aspect on resize and clamped to
760-1600. Fire input is latched on press, so a tap that starts and ends
inside a single frame still registers a shot.

Zombies carry two velocities: steering, which is capped at their walking
speed, and an external impulse, which is not. Explosion and bullet
knockback goes into the impulse channel and is scaled down by the target's
mass, so brutes shrug off hits that send runners flying.
