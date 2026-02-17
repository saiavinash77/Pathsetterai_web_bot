let conversationHistory = [];
const chatBox = document.getElementById('chat-box');
const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keydown', (e)=>{ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMessage(); } });

async function sendMessage(){
    const text = inputField.value.trim();
    if(!text) return;

    setInputState(true);
    addMessageToUI('user', text);
    conversationHistory.push({role:'user', content:text});
    inputField.value='';

    try{
        const res = await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({messages: conversationHistory})});
        if(!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();

        addMessageToUI('assistant', data.answer);
        conversationHistory.push({role:'assistant', content: data.answer});

    }catch(err){
        addMessageToUI('assistant', '⚠️ Error connecting to Alfred.');
        console.error(err);
    }finally{
        setInputState(false);
        inputField.focus();
    }
}

function setInputState(disabled){ inputField.disabled = disabled; sendBtn.disabled = disabled; }

function addMessageToUI(role, text){
    const wrap = document.createElement('div');
    wrap.className = 'message ' + (role==='user' ? 'user' : 'assistant');

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = role==='user' ? 'U' : 'A';

    const bubbleWrap = document.createElement('div');
    bubbleWrap.style.display = 'flex';
    bubbleWrap.style.flexDirection = 'column';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerText = text;

    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.innerText = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

    bubbleWrap.appendChild(bubble);
    bubbleWrap.appendChild(meta);

    wrap.appendChild(avatar);
    wrap.appendChild(bubbleWrap);

    chatBox.appendChild(wrap);
    chatBox.scrollTop = chatBox.scrollHeight;
}
