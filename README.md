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

## Campaign

Two modes from the main menu: **CAMPAIGN** and **ENDLESS**. Endless is the
original survival mode, untouched.

> **Test mode is currently ON.** `UNLOCK_ALL` at the top of the save section
> in `index.html` is set to `true`, so every world and stage is playable
> immediately and the world-select screen is tagged `TEST MODE: ALL UNLOCKED`.
> Set it to `false` to restore normal unlocking — stars, completion and best
> scores are earned and saved as usual while it is on, so flipping it back
> reveals real progress rather than resetting it.

Campaign runs **6 worlds x 5 stages**. Worlds and stages unlock strictly in
order: World 1 Stage 1 is open, clearing a stage opens the next, and clearing
a world's boss stage opens the next world. Nothing is entered by hand.

| World | Name | Theme |
|---|---|---|
| 01 | THE OUTBREAK | abandoned suburb |
| 02 | DEAD CITY | ruined city |
| 03 | NIGHTFALL | night, permanently dim |
| 04 | INFECTED FACTORY | industrial |
| 05 | THE QUARANTINE | hospital |
| 06 | THE WASTELANDS | open wasteland |

Themes are canvas-only (ground, grid, edge and tint colours) — no image assets.

**Stages** are fixed-length, not endless: 5 waves normally, 10 for a boss
stage. Enemy types are introduced one at a time across a stage's waves, and
the wave that introduces a type is weighted toward it, so you meet each new
threat on its own before it gets mixed in. World 1 Stage 1 runs walkers,
walkers, runner-heavy, mixed, then a special event.

**Special events** land on every 5th wave, announced before the wave starts:
BLOOD RUSH (many weak zombies), ZOMBIE FRENZY (much faster), BRUTE INVASION
(brutes only), BLACKOUT (vision cut to a light around you), INFECTION
(spitter-heavy).

**Bosses** hold the 5th stage of each world, appearing on the final wave with
a health bar across the top. World 1's is **THE BUTCHER** — 950 HP (5x a
brute), much larger, telegraphed charge attacks, summons zombies, and enters
a faster enraged state below 30% health.

**Stars** are 1-3 per stage: one for clearing it, one for finishing above 65%
health, one for 42%+ accuracy. A replay can only raise a rating, never lower
it.

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

## Save data

Two independent keys, so campaign progress and the endless high score never
interfere:

- `deadzone_best` — endless high score (pre-existing, untouched)
- `deadzone_campaign_v1` — unlocked/completed worlds and stages, best stars
  and best score per stage, highest endless wave
- `deadzone_sound` — sound on/off

The campaign save is merged over a freshly-generated blank structure on load,
so adding worlds or stages later will not wipe an existing save. Corrupt or
unavailable storage falls back to a new save rather than throwing.

Adding content means editing the `WORLDS` array (and `EVENTS` for new event
types) — the progression, unlock, star and save logic is generic over it.

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
