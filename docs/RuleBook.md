Card Types
==================

Monster
------------------
Monsters are the deck masters, each deck is built around a single monster card.
Monsters have the following on them:

* **HP** - or "Hit Points", this is how much damage the monster is able to take before it faints
* **ATK** - or "base attack", gets added to move attacks when attacking
* **DEF** - or "base defence", gets added to move defence when defending
* **Traits** - each monster has a number of skills, these are used when playing moves
* **Effect** - monsters can have an ability effect

Move
------------------
* **ATK** - the move's initial and/or added attack
* **DEF** - the move's initial and/or added defense
* **Traits** - move traits are cost for playing the move
* **Effect** - one or more special effects that the move has

### Types of moves ###
Moves are generally divided into types based on the timing in which they can be activated.

* **offensive** - offensive moves have ATK of 0 or more and DEF is marked with "~" and are plyed during your turn
* **defensive** - defensive moves have ATK maked as "~" and DEF of 0 or more and are plyed dururing the opponent's turn
* **dual** - dual moves have both ATK and DEF that is a number and can be used during either turn.
* **special** - special moves have both ATK and DEF marked as "~", their activation conditions are listed in the card text

In addition the stats can be divided into the following types:
* **initial** - the ATK and/or DEF is just a number, you can only play one initial move per attack or defense and it must be played before any additional moves
* **additional** - the ATK and/or DEF is a number with "+" or "-" in front, the move can be played at any time in the chain

#### Examples ####

* **"```ATK:3 / DEF:~```"**  - - offensive initial move
* **"```ATK:+1 / DEF:+1```"**   - - dual additional move
* **"```ATK:~ / DEF:~```"**   - - special move
* **"```ATK:~ / DEF:+0```"**   - - defensive additional move (no added points, presumably just effects)


Types of Effects
==================

Play
------------------
Play are the simplest type of effect, they activate as soon as the card is played.
(Monsters generally do not have play effects, if they do they activated once when the game starts)

Field
------------------
Field effects are not activated the turn they are played, instead they can be activated from the field after they have been moved from the staging zone.

Passive
------------------
Passive effects are effects that do not trigger, instead they have a continuous effect that remains active for as long as the card is in play.

Game Board
==================
The game board consists of 5 zones:
* Deck - is where the deck is placed
* Drop - is where cards go when used, discarded or destroyed
* Monster - is where the monster card is played
* Action - is where moves are played from the had or activated into from Stasis
* Stasis - is where cards with Field or Passive effects go to, during the cleanup
* Damage - is where cards tracking damage cards go

The action zone is further divided into attack (left) and defense (right).

Gameplay
==================

Glossary
------------------
**play**:	is the act of selecting a card in your hand and moving it into the action zone.
**activate**:	is when an effect is initiated e.g. due to the actions of players or game mechanics)
**initiate combat**:	is when a the turn player plays a move that starts a combat chain.

Setup (single battle)
------------------
Two players with a constructed deck.
The deck consists of 21 cards:
* 1 monster
* 20 moves

Both players place the monster card face up in front of them and shuffle the rest of the cards into the deck.

Both players then draw 5 cards and begin.

Player Turn
------------------
During your turn:
1. Alter - a special phase
1. Battle - play or activate moves as "attacks"
	a. The opponent has an opportunity to "defend"
2. Clear - the board
3. Draw - two cards from the deck

Playing a Move
------------------
You play moves from you hand by placing them into the action zone.
There are two times when you can play a move card from your hand - during your turn (*offensively*) and during your opponent's turn (*defensively*). Most moves can be played both ways but certain moves can only be played offensively and others only defensively. If a move can be activated during your turn it's **ATK** will be "0" or more, otherwise it will be marked with a tilde "~". Likewise a move can only be used defensively if its **DEF** stat is a number.

During your turn you can play *offensive* moves (ATK is not "~"). In addition you can only play moves that have an initial ATK stat, unless you initiate combat.

During your opponent's turn you can only play *defensive* moves (ATK is not "~") during combat or moves 

### Battle ###
If a move is played that has an initial **ATK** of at least "1" it must *initiate combat*. You can initiate combat only once per turn. As this happens the opponent's monster is targeted for attack and the offensive move starts a *combat chain*. The opponent then has an opportunity to respond with an initial defensive move. After this you have an opportunity to play an enhancing offensive move and then the opponent has another opportunity to play a defensive move. The chain builds this way going back and forth until neither player wants to play any more cards. The defending player can play only a single initial defense, but after that as many enhancing defense moves as they want.

Once the combat chain is built and neither player wishes to activate any more effects, the chain resolves backwards following the chain resolution rules.

After the chain is fully resolved final damage is calculated using the following formula

``` Final Damage = Final ATK / Final DEF ```

Rounded down to a whole number. Where 

``` Final ATK = Base Monster ATK + Initial Move ATK + Enhanced Move ATK ```

``` Final DEF = Base Monster DEF + Initial Move DEF + Enhanced Move DEF ```

If the final damage is 1 or more, the defending monster loses that much HP. If the final damage is 0, but the defending player did not use any defensive moves, the defending monster still takes 1 point of damage (called "direct attack damage"). For each point of damage the defender reveals the top card from their deck and places it face-up in the damage zone. When the number of cards in the damage zone becomes equal to the monster's HP that player looses the game.

**Attack and defense types**: when declaring an attack the traits of all offensive moves are considered to be the attack types. Likewise all defensive moves are considered to be defensive traits, however if the defending player does not play a defensive move, all monster traits become the defensive types.


### Out of Battle ###
As the turn player you can play non-combat moves. Non-combat moves have **ATK** of 0 and the opponent cannot respond to them with a defensive move. However the move starts a *non-combat chain*, if the opponent has any moves or effects that can trigger at this time and meet all activation requirements they can place them on the chain, and so on until neither player wishes to build the chain any further.

The chain resolves backwards following the chain resolution rules, but note that there is no damage calculation, all move stats from this chain are simply discarded.


Chain Resolution
------------------
Each time a chain is started and built up after players have agreed they don't want to activate effects any further it resolves backwards. Start from the last card that was played. If the card was played from the hand (vertical) its "Play" effect is activated (if any), if the card is horizontal its "Field" effect is activated. 



