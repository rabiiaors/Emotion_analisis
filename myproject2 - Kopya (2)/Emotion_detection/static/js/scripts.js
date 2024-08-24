// static/js/scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const emojis = ["🎉", "✨", "🎈", "🎊", "🎁", "🎂", "🎶", "🎵", "😊", "😃", "😉", "😍", "😎", "🤔", "🤩", "😂", "😘", "😢", "😡", "🤯", "🥳", "😴", "😱", "🥺", "😇", "😜"];

    for (let i = 0; i < 100; i++) {
        let emoji = document.createElement('div');
        emoji.className = 'emoji';
        emoji.style.top = Math.random() * 100 + '%';
        emoji.style.left = Math.random() * 100 + '%';
        emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
        document.querySelector('.background-effect').appendChild(emoji);
    }

    for (let i = 0; i < 50; i++) {
        let brightness = document.createElement('div');
        brightness.className = 'brightness';
        brightness.style.top = Math.random() * 100 + '%';
        brightness.style.left = Math.random() * 100 + '%';
        document.querySelector('.background-effect').appendChild(brightness);
    }
});
