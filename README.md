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

Each world is a distinct chapter — its own environment, atmosphere, zombie
designs and boss — all drawn on canvas with no image assets.

| World | Environment | Atmosphere | Zombie set | Boss |
|---|---|---|---|---|
| 01 THE OUTBREAK | suburban street, houses, fences, cars | warm dusk, drifting dust | `outbreak` — recognisable civilians | THE BUTCHER |
| 02 DEAD CITY | skyline, asphalt, burned cars, barricades | overcast, falling ash | `urban` — police, firefighter, construction | THE CRUSHER |
| 03 NIGHTFALL | graves, dead trees, street lamps | night, fog, a torch around you | `night` — silhouettes, **stalker**, **crawler** | THE NIGHT HUNTER |
| 04 INFECTED FACTORY | plating, conveyor, pipes, barrels, toxic pools | steam, flickering light | `industrial` — fused metal, acid sacs | THE ABOMINATION |
| 05 THE QUARANTINE | beds, containment tubes, biohazard marks | emergency red, bio motes | `experimental` — gowns, restraints, exposed cortex | PATIENT ZERO |
| 06 THE WASTELANDS | sand, sandbags, wrecks, crates | dust storm, harsh sun | `evolved` — bone plate, armour, helms | THE COLOSSUS |

Two enemies are exclusive to Nightfall: the **stalker**, which is nearly
invisible until it closes on you, and the low, fast **crawler**.

Visuals are data-driven. `WORLD_THEMES` holds palette, props, atmosphere and
lighting per world; `PROPS` holds one drawer per environment; `ZSKINS` holds
one art set per world; `BOSS_SKINS` holds one boss. Adding a world means
adding entries, not touching the renderer.

Stage layouts come from a seeded RNG (`world x stage`), so the five stages in
a world differ from each other but are identical every time you replay them.
Each stage also has its own environment name, shown on stage select.

**Stages** are fixed-length, not endless: 5 waves normally, 10 for a boss
stage. Enemy types are introduced one at a time across a stage's waves, and
the wave that introduces a type is weighted toward it, so you meet each new
threat on its own before it gets mixed in. World 1 Stage 1 runs walkers,
walkers, runner-heavy, mixed, then a special event.

**Special events** land on every 5th wave, announced before the wave starts:
BLOOD RUSH (many weak zombies), ZOMBIE FRENZY (much faster), BRUTE INVASION
(brutes only), BLACKOUT (vision cut to a light around you), INFECTION
(spitter-heavy).

A **world intro** plays the first time you enter a world, and a full-screen
**boss warning** precedes the boss walking in.

**Bosses** hold the 5th stage of each world, appearing on the final wave with
a health bar across the top. World 1's is **THE BUTCHER** — 950 HP (5x a
brute), much larger, telegraphed charge attacks, summons zombies, and enters
a faster enraged state below 30% health. Each world's boss has its own
silhouette; behaviour is shared and scaled.

**Stars** are 1-3 per stage: one for clearing it, one for finishing above 65%
health, one for 42%+ accuracy. A replay can only raise a rating, never lower
it.

## How it plays

Zombies spawn off-screen and close in from every edge. Clear the wave, get a
short breather plus a bonus, then the next wave starts — bigger, faster, tougher.
Each wave scales enemy count, health, and speed, and mixes in nastier types.

**Enemies** — ten types, introduced gradually across the campaign.

| Enemy | Threat | First appears |
|---|---|---|
| Walker | slow, common | W1 S1 |
| Runner | fast, fragile | W1 S2 |
| Brute | heavy, high HP | W1 S4 |
| Spitter | ranged, lobs acid | W2 S3 |
| Crawler | low, very fast, small target | W2 S4 |
| Exploder | charges, telegraphs, detonates — hurts zombies too | W3 S3 |
| Stalker | near-invisible until it closes | W3 S4 |
| Screamer | hangs back, calls reinforcements after a warning | W4 S2 |
| Shield zombie | armoured to the front; flank it | W4 S3 |
| Tank | enormous, slow, shoves you backwards | W5 S3 |

Nothing outside a stage's table can spawn, so World 1 cannot produce a tank
no matter how the dice fall. Within a stage, early waves lean on basics and
specials ramp up toward the last wave. Concurrency limits cap how many of
each specialist can be alive at once (1 tank, 1 screamer, 3 exploders, 6
specials total, 46 enemies overall), so a bad roll can never stack four
tanks or an endless screamer chain.

Endless keeps a **separate** ladder that unlocks types by wave number, so it
still starts simple and reaches the full roster around wave 21.

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
Each of the three locks while its own effect runs: a second press — click,
double-click, held key, or rapid tap — is ignored outright and costs no
charge. The card dims and shows a progress strip until the effect ends. The
lock is derived from state each ability already keeps (a grenade in flight,
the shield expiry, the blast cooldown), so it can never disagree with what
is actually happening.

- **Power blast** (`Q`) — an instant 210px shockwave centered on you.
  Heavy damage with falloff plus a hard shove outward, and it never hurts
  you. Clears a surrounding pack of walkers outright. Short cooldown so one
  press spends exactly one charge.

**Scoring** — kills award points, and a kill streak builds a combo multiplier
(up to 2.5x) that decays if you stop killing. Clearing a wave pays a bonus
scaled by wave number and remaining health. Best score persists in
`localStorage`.

**Drops** — dead zombies sometimes leave medkits (+25 HP) or ammo boxes.

## Power-ups

**Magnet** — a horseshoe magnet dropped by zombies. Collecting it activates
immediately (no key, no button, works the same on desktop and touch) and for
10 seconds every collectible within 250px accelerates toward you and is
picked up normally. Items track your live position, so they follow you while
you move, and a drop created *during* the effect is pulled in straight away.

Collecting a second magnet while one is running **refills the timer to full
rather than stacking** — there is only ever one effect. When it expires,
attraction stops and any items that never reached you stay on the ground as
ordinary pickups.

Drop chance is per enemy class: 3.5% from normal zombies, 9% from brutes,
guaranteed from a boss. The roll is separate from the gear roll, so a magnet
never displaces an ammo or health drop.

All of it is tuned from one table:

```js
const MAGNET_CONFIG = {
  duration: 10000, radius: 250, accel: 0.55, maxSpeed: 7.5,
  drop: { normal: 0.035, brute: 0.09, boss: 1.0 }
};
```

Timed effects live in a `POWERUPS` registry that the pickup, HUD and drop
systems are generic over, so a future speed or damage boost is a new entry
plus its art — not a change to the pickup system.

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

## Rendering cost

Static props are drawn once per stage into an offscreen canvas and blitted
each frame, and atmosphere uses a fixed pre-allocated pool that wraps rather
than respawning. Measured at a 844x390 mobile viewport with 26 zombies and
40 particles, `render()` costs 0.17ms in endless and 0.22-0.49ms in the
themed worlds — 1-3% of a 60fps frame. A prop-layer rebuild costs
0.10-0.24ms and happens only on stage or viewport change.

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
