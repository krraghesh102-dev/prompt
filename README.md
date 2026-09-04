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
| `X` | Air strike — then click a target (`Esc` / right-click cancels) |
| `P` / `Esc` | Pause / resume |

## On a phone

Play it in **landscape** — the game shows a rotate prompt and pauses in portrait.

Twin-stick controls. Both sticks **float**: they appear wherever your thumb
lands, so there is no fixed pad to hunt for.

| Touch | Action |
|---|---|
| **Left half** — drag anywhere | Move in any direction; push far to sprint |
| **Right half** — drag anywhere | Aim in that direction and fire continuously |
| **Right half** — quick tap | Fire at the exact spot you tapped |
| On-screen buttons (top-left) | Weapon slots, reload |
| Pause button (top-right) | Open the pause menu |
| On-screen buttons (bottom-right) | Grenade, shield, power blast, air strike |

Both thumbs work at once, so you can retreat while firing behind you.

Because aim on the right stick is a *direction* rather than a screen
position, every heading is reachable — including straight back over the
hand that is moving you. The playfield width follows the screen aspect
ratio, so the game fills a phone edge to edge.

## Pausing

Press `P` or `Esc`, or hit the **pause button in the top-right of the HUD** —
it is drawn on desktop and mobile alike, and sized to a comfortable tap
target on a phone.

Pausing freezes the whole simulation, not just movement. `game.state` is the
only thing that decides whether gameplay is running: `update()` is called
solely in the `play` state, so zombie AI, spawning, wave and break timers,
ability durations, magnet, reload, burn and freeze, stamina, projectiles in
flight and the combo timer all stop together and cannot drift apart. The
battlefield stays visible behind the dimmed panel. Resuming rebases the
frame clock, so time spent paused is never delivered as one huge delta.

The menu offers four choices:

| Option | Effect |
|---|---|
| **RESUME GAME** | Back to play immediately |
| **RESTART STAGE** | Rebuilds the current stage from the start |
| **QUIT GAME** | Leaves the stage for the stage-select screen |
| **GO TO MENU** | Back to the main menu |

The last three ask for confirmation first; **CANCEL** returns to the pause
menu with the game still frozen. Restarting a stage rebuilds only stage
state — unlocked weapons, banked upgrades, stars and campaign progress live
in the save and are untouched.

While the pause menu or a confirmation is open, no click or touch reaches
the canvas: the overlay covers it, the canvas handlers ignore input outside
the `play` state, and any key or thumb held at the moment of pausing is
released so resuming cannot fire a stray shot or keep walking. A
confirmation also ignores input for a quarter-second after opening, so the
second tap of a double-tap on a menu button cannot answer the dialog that
tap just opened.

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

**Armory** — three guns, plus four limited-charge items.

*Guns* — nine weapons, unlocked across the campaign. Each has a distinct job;
none is simply a better version of the last.

| Weapon | Role | Unlocks | Key mechanic |
|---|---|---|---|
| Pistol | reliable all-rounder | start | infinite reserve |
| Shotgun | close burst | W1 S3 | 7 pellets, heavy knockback |
| Rifle | sustained damage | W1 S5 | full-auto |
| Sniper | precision | W2 S2 | **pierces 3 enemies**, x3 headshots, laser sight |
| Grenade launcher | area denial | W3 S1 | lobbed shell, 120px blast |
| Flamethrower | crowd burn | W4 S1 | cone stream + burn that outlasts the flame |
| Tesla | chain damage | W4 S4 | jumps to 4 targets, 0.78 falloff per jump |
| Rocket | heavy burst | W5 S3 | 215px blast, 1 in the tube, 10 in reserve |
| Freeze | crowd control | W6 S1 | freezes for 1.5s; bosses resist (0.24s) |

Player explosives never damage the player. Headshots multiply damage per
weapon (`headMul`), and bosses cap the bonus so they can't be trivialised.

Weapons are switched with **1-9**, **E/Z** to cycle, or by tapping the slots
on touch — only unlocked weapons get a slot, and the row wraps.

Ammo comes in two tiers from the existing drop system: a common box for the
standard guns and a rarer crate for the heavy weapons, both favouring the
weapon you're holding. Unlocks are permanent and saved.

*Gear* — each has limited charges, shown bottom-right. Charges drop from
kills and top up between waves (a grenade every wave, a shield every third,
a blast every fourth, an air strike every sixth).

- **Grenade** (`G`) — thrown along your aim, ~0.8s fuse, bounces off walls.
  118px blast with damage falling off to the rim. It **will hurt you** at
  half damage if you are inside the radius, so mind the bounce.
- **Security layer** (`F`) — a full-body barrier that absorbs *all* damage
  for 6.5 seconds, bites and acid included. A ring around you counts the
  time down. Using it while already up extends the timer rather than
  restarting it, so a charge is never wasted.
Each of the four locks while its own effect runs: a second press — click,
double-click, held key, or rapid tap — is ignored outright and costs no
charge. The card dims and shows a progress strip until the effect ends. The
lock is derived from state each ability already keeps (a grenade in flight,
the shield expiry, the blast cooldown, the air strike phase), so it can
never disagree with what is actually happening. Air strike holds its lock
across the *whole* call-in — targeting, the approach, every explosion and
the settle — and its charge is spent only when the target is confirmed.

- **Power blast** (`Q`) — an instant 210px shockwave centered on you.
  Heavy damage with falloff plus a hard shove outward, and it never hurts
  you. Clears a surrounding pack of walkers outright. Short cooldown so one
  press spends exactly one charge.
- **Air strike** (`X`) — the ranged one. Unlocked at **World 2 Stage 1**,
  max 2 charges, and its card only appears once the campaign has granted it
  (the same rule the weapon slots use). Pressing it opens *targeting*, it
  does not drop anything: a dashed radius and reticle follow your cursor
  (or your thumb), clamped to the battlefield. Confirm and an aircraft runs
  in from the side and walks **six** explosions across the target, each
  announced by a closing ground marker a moment before it lands. 86px
  radius and 130 damage per bomb, overlapping enough that a single target
  takes two or three of them; it never hurts you.

  Where blast is instant and centred on you, air strike is delayed, aimed
  and much wider — a crowd and boss answer rather than a panic button.
  Cancelling before you confirm (`Esc`, right-click, or the on-screen
  CANCEL) costs nothing.

  | Input | Targeting | Confirm | Cancel |
  |---|---|---|---|
  | Desktop | mouse moves the reticle | left click | `Esc` or right-click |
  | Mobile | tap or drag to place | tap again | CANCEL button |

  While targeting, the weapon will not fire and the rest of the gear row is
  inert, so a stray tap cannot throw a grenade mid-aim. `Esc` cancels
  targeting rather than pausing. It starts with no charges — unlike the
  other three — so the first one is earned from a wave top-up or a drop.

  Pausing mid-call-in freezes the aircraft, the warning timers and the
  remaining explosions, and resuming continues from the same point rather
  than skipping ahead; the impact points are decided at confirmation, so a
  pause cannot reshuffle where the bombs land.

## Combat feel

Every number that decides how much punch a hit has lives in
`COMBAT_FEEDBACK_CONFIG` and `SCREEN_SHAKE_CONFIG` near the top of the
combat section, so the feel can be tuned in one place. Per-weapon fire
shake and recoil deliberately stay on the `WEAPONS` rows — they are weapon
data, and copying them into a second table would give the game two sources
of truth.

The chain a player should read without thinking: **shot → impact → damage →
reaction → kill → score → combo.**

- **Muzzle flash** — a drawn petal, hot core and soft bloom at the barrel,
  sized from the weapon's own recoil value, plus drifting smoke for the
  heavy weapons. The pistol pops, the shotgun blooms, the rifle ticks.
- **Recoil** is visual only: the sprite kicks back along the aim and
  recovers. It never moves your point of aim.
- **Hit flash** — every enemy type lights for 110ms, a head hit for 190ms,
  and a **boss only 55ms** so its tells stay readable.
- **Impact** — directional blood that continues along the shot rather than
  puffing symmetrically. Shotgun pellets contribute half each, so a full
  seven-pellet blast is not seven times the spray.
- **Headshots** — bigger burst from the head itself, longer flash, 1.5x the
  shove, a short camera snap, a distinct sound and a `HEADSHOT` label. A
  *lethal* head hit adds its own directional burst and a screen bloom; a
  non-lethal one does not play the death effect.
- **Floating text** is throttled per label kind (`floatThrottleMs`), so
  automatic fire cannot stack twenty `HEADSHOT`s on top of each other —
  while still counting every one. Score floats are never throttled: one
  kill is one number.
- **Combo tiers** announce at every fifth kill with the multiplier the
  scoring already applies (`5x COMBO 1.25x`). They award nothing; they just
  say out loud what already happened. Expiry is a quiet one-line float.
- **Multi-kill** — four kills inside 420ms calls `MULTI KILL`, seven calls
  `MASSACRE`.
- **Screen shake** is short and bounded (cap 30, ~0.88 decay per frame).
  Kill shakes damp against the recent-kill count, so an explosion taking a
  dozen enemies does not stack a dozen shakes into a long rattle.
- **Slow motion** is deliberately rare: a boss kill or a four-kill burst,
  130ms at 0.35 speed. It scales the single frame delta every timer is
  derived from, so nothing drifts out of step, and it burns down inside
  `update()` — pausing freezes it like everything else. An ordinary
  headshot never triggers it.
- **Death animations** — each type falls differently (`DEATH_STYLES`): the
  runner pitches forward, the brute topples slowly, the spitter leaks
  purple. A corpse is a **separate object that never enters `zombies`**, so
  it cannot be hit, cannot attack, and cannot score, drop or die a second
  time however long its animation runs. The list is capped at 22.

*Mobile* runs the same feedback at `fxScale()` = 0.6 — fewer particles and
a calmer camera, with every flash, label, shake and sound still firing.
Nothing is removed. Measured on a 844x390 viewport with 30 enemies,
sustained fire and headshot kills: worst frame 4.2ms against a 16.7ms
budget.

**Scoring** — kills award points, and a kill streak builds a combo multiplier
(up to 2.5x) that decays if you stop killing. Clearing a wave pays a bonus
scaled by wave number and remaining health. Best score persists in
`localStorage`.

**Drops** — dead zombies sometimes leave medkits (+25 HP) or ammo boxes.

## Collectibles

Health, ammo, and the gear charges keep exactly the drop rates they always
had. The valuables below roll **separately**, the way the magnet already
did, so nothing new can push an existing drop out of the table.

| Drop | What it does | Base chance |
|---|---|---|
| ❤ **Heart** | +1 life (never HP) | 1.5% |
| ● **Coins** | 5–25 banked currency | 8% |
| 🔥 **Damage boost** | ×2 weapon damage, 10s | 2.5% |
| ⧗ **Slow motion** | game runs at 45%, 6s | 1.5% |
| ◆ **Rare gem** | +100 gems | 0.3% |

Each has its own silhouette, not just its own colour — a beating heart, a
spinning coin, a flame, a draining hourglass, a faceted crystal — so they
stay apart on a small screen. Stronger enemies bias the rolls (`DROP_BIAS`):
brutes drop more coins and boosts, spitters more slow motion, stalkers more
gems. A boss is the one guaranteed payday (`BOSS_DROPS`) — coins and a heart
every time, the rest on good odds, deliberately *not* everything at once.

**Lives** are run-scoped, not saved: you start with 3. Dying with a life in
hand spends it and revives you in place at 60% health with 2.2s of grace and
a shove that clears the pack, instead of ending the run; at zero it is the
normal game-over flow, and Retry is untouched. Capped at 9 — a heart at the
cap pays score instead. Works the same in campaign and endless.

**Coins and gems are separate currencies**, banked the instant you touch the
pickup and never rolled back — not on death, not on a stage restart, not on
a world change. They live in the existing campaign save (`coins`, `gems`); a
save written before they existed loads with zero and keeps everything else.

**Damage boost** multiplies through `damageMul()`, the one value every
weapon damage path reads — the shared `damageEnemy()` and the shell/rocket
blast. It never writes to a saved upgrade level, and a second pickup while
one is running refills the timer without touching the multiplier (measured:
26 → 52 damage, still 52 after a second pickup, back to 26 on expiry).

**Slow motion** drives the same single real-time scale the loop already
owned for its combat flourishes, so there is one time scale and it is never
compounded. Gameplay reads the scaled delta; the effect's own countdown uses
*real* time, because a duration measured in the slowed clock would stretch
itself (measured: 6000ms configured, 6006ms elapsed). Input, menus and pause
stay on real time, and pausing freezes it like everything else. It is a
pickup, not a fifth ability — it adds no button and spends no charge.

Every collectible is magnetic, including all five new ones; zombies, bosses,
bullets and spits are not. Tuning lives in `DROP_CONFIG`, `DROP_BIAS`,
`BOSS_DROPS`, `LIFE_CONFIG`, `COIN_CONFIG`, `GEM_CONFIG`,
`DAMAGE_BOOST_CONFIG` and `SLOW_MOTION_CONFIG`.

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

## Upgrades

**Every stage opens with the choice**, boss stages included — including the
very first stage of the campaign. The stage is built and then held:
`game.state` is `"upgrade"` and `update()` only runs in `"play"`, so wave 1
cannot begin behind the popup. Pick one of three and the stage starts.

The grant is recorded on the stage's own save entry, so quitting and
re-entering the same stage does not hand out a second upgrade; a stage you
have never played always offers one. A save written before this carries no
flag, and a stage already cleared counts as having had its pick.

Progression is meant to read as *my weapons are getting better*, not *my
streak is getting longer*. The combo is still a **score** bonus (1x → 2.5x)
and still announces its tiers, but as a small float rather than a banner —
the power curve is the upgrades.

Upgrades have four rarities — common, rare, epic, legendary — which set both
how big the step is and how often it is offered. The tier is rolled first and
an entry picked inside it, so the handful of epics are not drowned out by the
many commons. Boss stages shift the weights upward (measured: epic 9.7% to
18.5%, legendary 2.9% to 9.4%).

The three cards are drawn only from upgrades you can actually use. An entry
declares either a `weapon` (must be unlocked, read from live progression —
not from the weapon table's existence) or a `feature` (must be active), and
anything already at level 5 leaves the pool. The remainder is shuffled and
three are taken, preferring three different categories.

Offers lean toward combat. Rarity still picks the tier; a category priority
table then picks the row inside it, so roughly three quarters of what you
are shown makes your shooting stronger while survival and utility stay in
the mix. No two cards in an offer share a category, so you never get the
same stat three times.

Every row changes real gameplay, never a displayed number — measured
end to end at level 3:

| Upgrade | Effect |
|---|---|
| Damage | 26 → 33.8 |
| Fire rate | 210ms → 165.9ms between shots |
| Accuracy | 0.035 → 0.022 rad spread |
| Reload | 900ms → 684ms |
| Magazine | 12 → 18 rounds |
| Round speed | 14 → 19 px/frame |
| Knockback | 3 → 4.35 |
| Range | ×1.3 bullet life |
| **Multi shot** | 1 → 3 rounds per trigger pull |
| Crit chance / damage | 0 → 12% · ×1.5 → ×1.95 |
| Piercing | 0 → 3 enemies |
| Grenade / blast / layer | damage, radius and duration all scale |

**Multi shot** is the headline one: one trigger pull, one round of ammo,
several bullets fanned either side of the aim. Each is an ordinary
independent `Bullet` carrying full damage through the same single collision
path, so a three-round volley into one enemy still kills once, scores once
and drops once. The **shotgun is deliberately excluded** — it already fires
a pellet spread, and stacking a multiplier on that is the duplicate-pellet
trap; stream and chain weapons have no single projectile to duplicate.

Categories: per-weapon damage / fire rate / reload / magazine / accuracy /
multi shot / knockback / round speed / ammo capacity / range, plus
weapon-specific ones (shotgun pellets, sniper crit damage, blast radius and
shell speed, burn duration, tesla chain count and range, freeze duration);
ability rows for grenade, blast and the security layer; player health,
armor, move speed, stamina and sprint recovery; crit chance, crit damage and knockback;
ammo and medkit potency; magnet duration and range. Universal rows
(**Weapon Mastery**, **Combat Training**, **Fast Hands**) improve every
unlocked weapon at once and are rarer. Legendary behaviour upgrades change
how a weapon works: **piercing rounds**, **vampiric ammo**, **incendiary
rounds** — new ones are an entry plus the single hook that honours it.

Endless keeps a **separate, run-scoped** upgrade set, so nothing earned in a
run touches campaign progression, and campaign levels do not carry into a
run. Endless still inherits unlocked weapons.

Armor and crit chance are hard-capped at 20%. Magnet upgrades only appear
once you have actually collected a magnet. Levels are saved in the campaign
save, survive reload, stage changes, world changes and replays, and carry
into endless.

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
