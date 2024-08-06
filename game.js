const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Set canvas size dynamically
function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

// Game settings
const playerSize = 50;
const playerSpeed = 5;
const laserSpeed = 10;
const enemySize = 50;
const laserWidth = 5;
const laserHeight = 20;

// Initialize game state
let playerX = canvas.width / 2 - playerSize / 2;
let playerY = canvas.height - playerSize - 10;
let lasers = [];
let enemies = [];
let lastShotTime = 0;
const reloadTime = 500; // milliseconds
let difficultyLevel = 1;
const difficultyInterval = 5000; // milliseconds

// Handle player movement
function movePlayer(dx) {
  playerX += dx;
  if (playerX < 0) playerX = 0;
  if (playerX > canvas.width - playerSize) playerX = canvas.width - playerSize;
}

// Handle laser shooting
function shootLaser() {
  const now = Date.now();
  if (now - lastShotTime > reloadTime) {
    lasers.push({ x: playerX + playerSize / 2 - laserWidth / 2, y: playerY });
    lastShotTime = now;
  }
}

// Update game state
function update() {
  // Move lasers
  lasers = lasers
    .map((laser) => ({ x: laser.x, y: laser.y - laserSpeed }))
    .filter((laser) => laser.y > 0);

  // Spawn enemies
  if (Math.random() < 0.05) {
    // 5% chance to spawn an enemy
    const enemyX = Math.random() * (canvas.width - enemySize);
    enemies.push({ x: enemyX, y: 0 });
  }

  // Move enemies
  enemies = enemies
    .map((enemy) => ({ x: enemy.x, y: enemy.y + (5 + difficultyLevel) }))
    .filter((enemy) => enemy.y < canvas.height);

  // Check collisions
  function detectCollision(ax, ay, aw, ah, bx, by, bw, bh) {
    return ax < bx + bw && ax + aw > bx && ay < by + bh && ay + ah > by;
  }

  lasers.forEach((laser) => {
    enemies.forEach((enemy, idx) => {
      if (
        detectCollision(
          laser.x,
          laser.y,
          laserWidth,
          laserHeight,
          enemy.x,
          enemy.y,
          enemySize,
          enemySize
        )
      ) {
        lasers = lasers.filter((l) => l !== laser);
        enemies.splice(idx, 1);
      }
    });
  });

  enemies.forEach((enemy) => {
    if (
      detectCollision(
        playerX,
        playerY,
        playerSize,
        playerSize,
        enemy.x,
        enemy.y,
        enemySize,
        enemySize
      )
    ) {
      alert("Game Over!");
      document.location.reload();
    }
  });
}

// Draw everything
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player
  ctx.fillStyle = "blue";
  ctx.fillRect(playerX, playerY, playerSize, playerSize);

  // Draw lasers
  ctx.fillStyle = "red";
  lasers.forEach((laser) =>
    ctx.fillRect(laser.x, laser.y, laserWidth, laserHeight)
  );

  // Draw enemies
  ctx.fillStyle = "green";
  enemies.forEach((enemy) =>
    ctx.fillRect(enemy.x, enemy.y, enemySize, enemySize)
  );
}

// Main game loop
function gameLoop() {
  update();
  draw();
  requestAnimationFrame(gameLoop);
}

// Add touch controls
const controlPanel = document.createElement("div");
controlPanel.style.position = "fixed";
controlPanel.style.bottom = "0";
controlPanel.style.left = "0";
controlPanel.style.width = "100%";
controlPanel.style.display = "flex";
controlPanel.style.justifyContent = "space-between";
controlPanel.style.padding = "10px";
controlPanel.style.boxSizing = "border-box";

const moveLeftButton = document.createElement("button");
moveLeftButton.innerText = "←";
moveLeftButton.style.flex = "1";
moveLeftButton.style.fontSize = "24px";
moveLeftButton.addEventListener("touchstart", () => movePlayer(-playerSpeed), {
  passive: false,
});
moveLeftButton.addEventListener("touchend", () => movePlayer(0), {
  passive: false,
});
moveLeftButton.addEventListener("touchcancel", () => movePlayer(0), {
  passive: false,
});

const shootButton = document.createElement("button");
shootButton.innerText = "Shoot";
shootButton.style.flex = "1";
shootButton.style.fontSize = "24px";
shootButton.addEventListener("touchstart", () => shootLaser(), {
  passive: false,
});

const moveRightButton = document.createElement("button");
moveRightButton.innerText = "→";
moveRightButton.style.flex = "1";
moveRightButton.style.fontSize = "24px";
moveRightButton.addEventListener("touchstart", () => movePlayer(playerSpeed), {
  passive: false,
});
moveRightButton.addEventListener("touchend", () => movePlayer(0), {
  passive: false,
});
moveRightButton.addEventListener("touchcancel", () => movePlayer(0), {
  passive: false,
});

controlPanel.appendChild(moveLeftButton);
controlPanel.appendChild(shootButton);
controlPanel.appendChild(moveRightButton);

document.body.appendChild(controlPanel);

// Start the game
gameLoop();
