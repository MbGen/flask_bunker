var socket = io();
socket.on('connect', function() {
    socket.emit('join', {room_id: '{{ lobby_id }}', username: '{{ g.user.username }}', user_id: '{{ g.user.id }}'});
});

socket.on('json', data => {
  if (sessionStorage.getItem('user_id') !== data.userId){
    showPlayerCard(data)
  }
});

function showPlayerCard(data) {
   $('#player_card').append(`<div class="cell">
      <div class="card" style="width: 300px;">
        <div class="card-divider">
          This is card of player
        </div>
        <div class="card-section">
          <h4>Player id - ${data.userId} </h4>
          <p>Player Name - ${data.username}  </p>
        </div>
      </div>
  </div>`);
} 