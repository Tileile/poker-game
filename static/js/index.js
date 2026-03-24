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
    for (const card in infoJSON['cards']){
      const img = document.getElementById(card)
      const cardImg = infoJSON['cards'][card]
      console.log(typeof(card), card, cardImg)
      img.src = cardImg

    // bot ID prefixes
    const botPrefixes = ['bot-', 'bot2-', 'bot3-'];

    // For each bot prefix, update the card images
    botPrefixes.forEach(prefix => {
      const pId = `${prefix}${card}`;
      const img = document.getElementById(pId);
      if (img) img.src = BACKSIDE_IMG;
    });

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

    const bots = [
      { key: 'bot_cards', prefix: 'bot-' },
      { key: 'bot2_cards', prefix: 'bot2-' },
      { key: 'bot3_cards', prefix: 'bot3-' }
    ];

    bots.forEach(bot => {
      const cards = infoJSON[bot.key]['cards'];
      for (const card in cards) {
        const pId = `${bot.prefix}${card}`;
        const img = document.getElementById(pId);
        if (img) img.src = cards[card];
      }
    });

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


