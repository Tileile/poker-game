'use strict'

// Tracks state of game, so player cant do illegal moves, for cosmetic reasons/error messages.
// Backend prevents illegal moves anyway.
let gameState = 'created'

const startBtn = document.getElementById('start-btn')
startBtn.addEventListener('click', () => StartNewGame(1))

//handles Start Game -button press
async function StartNewGame(jokers) {
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/start_game/${jokers}`);
    if (!response.ok) throw new Error('loading card info failed');
    const infoJSON = await response.json();
    gameState = 'start'
    clearHold()
    console.log(infoJSON)
    //tee tänne jotain, lisää kortit kuvina pöydälle
    for (const card in infoJSON['cards']){
      const img = document.getElementById(card)
      const cardImg = infoJSON['cards'][card]
      console.log(typeof(card), card, cardImg)
      img.src = cardImg

      /*insert backside images of bot cards*/
      let pId = `bot-${card}`
      const img2 = document.getElementById(pId)
      img2.src = `PNG-cards-1.3/backside.png`

      /*insert backside images of bot2 cards*/
      let pId2 = `bot2-${card}`
      const img3 = document.getElementById(pId2)
      img3.src = `PNG-cards-1.3/backside.png`

      /*insert backside images of bot2 cards*/
      let pId3 = `bot3-${card}`
      const img4 = document.getElementById(pId3)
      img4.src = `PNG-cards-1.3/backside.png`

    }
    const action_line = document.getElementById('action-line')
    action_line.innerText = `Choose cards to hold and press Switch`
  } catch (error) {
    console.log(error.message);
  }
}

const switchBtn = document.getElementById('switch-btn')
switchBtn.addEventListener('click', switchCards)

// handles Switch-button press
async function switchCards() {
  // get hold bits, 0 = fold, 1 = hold
  const cards = Array.from(document.getElementsByClassName('p1'));
  const binary_values = cards.map(card => card.dataset.value).join('')
  console.log(binary_values)
  try {
    const response = await fetch(
        `http://127.0.0.1:3000/switch/${encodeURIComponent(binary_values)}`);
    if (!response.ok) throw new Error('loading card info failed');
    const infoJSON = await response.json();
    gameState='switch'
    clearHold()
    for(const card of infoJSON['cards']){
      console.log(card)
      for (const info of card){
        console.log(`suit ${info['suit']}, rank ${info['rank']} `)
      }
    }

    // change card images for player
    for (const card in infoJSON['p_cards']['cards']){
      const img = document.getElementById(card)
      img.src = infoJSON['p_cards']['cards'][card]
    }
    //change card images for bot (reveals bots cards)
    for (const card in infoJSON['bot_cards']['cards']){
      let pId = `bot-${card}`
      const img = document.getElementById(pId)
      img.src = infoJSON['bot_cards']['cards'][card]
    }

    //change card images for bot2 (reveals bots cards)
    for (const card in infoJSON['bot2_cards']['cards']){
      let pId = `bot2-${card}`
      const img = document.getElementById(pId)
      img.src = infoJSON['bot2_cards']['cards'][card]
    }

    //change card images for bot2 (reveals bots cards)
    for (const card in infoJSON['bot3_cards']['cards']){
      let pId = `bot3-${card}`
      const img = document.getElementById(pId)
      img.src = infoJSON['bot3_cards']['cards'][card]
    }

    const win_line = document.getElementById('action-line')

    //win_line.innerText = `P${parseInt(infoJSON['winner_index']) + 1} wins with ${infoJSON['hand_name']}. \n Press Start Game`
    win_line.innerText = get_win_line(infoJSON['winner_index'], infoJSON['hand_name'])
  } catch (error) {
    console.log(error.message);
  }
}

function get_win_line(winners, hand_name) {
  let line = ''
  if (winners.length > 1){
    line += 'Game is tie, '
    for (const winner of winners){
      line += `P${parseInt(winner)+1} `
    }
  }
  else{
    line = `P${parseInt(winners[0])+1} `
  }
  line += `wins with ${hand_name}. Press Start Game`
  return line


}

//toggles hold icons when player clicks on card
function toggleCard(card) {
  //ensures hold icon isn't shown after game has ended
  if(gameState==='start'){
    const text = `hold${card.dataset.index}`
    const hold = document.getElementById(text)
    // flip hold bit and hide hold icon
    if(card.dataset.value === '1') {
      card.dataset.value = '0'; //hold bit
      hold.classList.add('hide');
     } else { //otherwise show hold icon and flip hold bit
      card.dataset.value = '1';
      hold.classList.remove('hide');
    }
  }
}

//clear all hold icons and set hold bits to 0, used after switch/game end
function clearHold(){
  const cards = Array.from(document.getElementsByClassName('p1'));
  for (const card of cards) {
    if (card.dataset.value === '1') {
     const text = `hold${card.dataset.index}`
     const hold = document.getElementById(text)
     card.dataset.value = '0';
     hold.classList.add('hide')
   }
 }
}


