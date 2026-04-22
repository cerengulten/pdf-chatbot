const API = 'http://localhost:8000'

// Elements
const dropZone      = document.getElementById('drop-zone')
const fileInput     = document.getElementById('file-input')
const uploadStatus  = document.getElementById('upload-status')
const uploadSection = document.getElementById('upload-section')
const chatSection   = document.getElementById('chat-section')
const docName       = document.getElementById('doc-name')
const messages      = document.getElementById('messages')
const questionInput = document.getElementById('question-input')
const sendBtn       = document.getElementById('send-btn')
const resetBtn      = document.getElementById('reset-btn')
let chatHistory = []
// ── Upload ────────────────────────────────────────────────

dropZone.addEventListener('click', () => fileInput.click())

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) uploadFile(fileInput.files[0])
})

dropZone.addEventListener('dragover', e => {
  e.preventDefault()
  dropZone.classList.add('dragover')
})

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover')
})

dropZone.addEventListener('drop', e => {
  e.preventDefault()
  dropZone.classList.remove('dragover')
  const file = e.dataTransfer.files[0]
  if (file && file.name.endsWith('.pdf')) uploadFile(file)
  else setStatus('Please drop a PDF file.', 'error')
})

async function uploadFile(file) {
  setStatus('Uploading and indexing...', '')
  sendBtn.disabled = true

  const form = new FormData()
  form.append('file', file)

  try {
    const res = await fetch(`${API}/upload`, { method: 'POST', body: form })
    const data = await res.json()

    if (!res.ok) throw new Error(data.detail || 'Upload failed')

    setStatus(`Indexed ${data.chunks} chunks from "${file.name}"`, 'success')
    docName.textContent = file.name
    uploadSection.classList.add('hidden')
    chatSection.classList.remove('hidden')
    questionInput.focus()
  } catch (err) {
    setStatus(err.message, 'error')
  } finally {
    sendBtn.disabled = false
  }
}

function setStatus(msg, type) {
  uploadStatus.textContent = msg
  uploadStatus.className = 'upload-status ' + type
}

// ── Chat ──────────────────────────────────────────────────

sendBtn.addEventListener('click', sendQuestion)

questionInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) sendQuestion()
})

async function sendQuestion() {
  const question = questionInput.value.trim()
  if (!question) return

  addBubble(question, 'user')
  questionInput.value = ''
  sendBtn.disabled = true

  const loading = addBubble('Thinking...', 'loading')

  try {
    const res = await fetch(`${API}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, history: chatHistory })
    })
    const data = await res.json()

    loading.remove()

    if (!res.ok) throw new Error(data.detail || 'Something went wrong')

    addBubble(data.answer, 'bot')
    addSources(data.sources)

    // append to history
    chatHistory.push({ role: 'user', content: question })
    chatHistory.push({ role: 'assistant', content: data.answer })
  } catch (err) {
    loading.remove()
    addBubble(`Error: ${err.message}`, 'bot')
  } finally {
    sendBtn.disabled = false
    questionInput.focus()
  }
}

function addBubble(text, type) {
  const div = document.createElement('div')
  div.className = `bubble ${type}`
  div.textContent = text
  messages.appendChild(div)
  messages.scrollTop = messages.scrollHeight
  return div
}

function addSources(sources) {
  if (!sources || sources.length === 0) return

  const wrapper = document.createElement('div')
  wrapper.className = 'sources'

  const toggle = document.createElement('button')
  toggle.className = 'sources-toggle'
  toggle.textContent = `Show ${sources.length} sources`

  const list = document.createElement('div')
  list.className = 'sources-list'

  sources.forEach((src, i) => {
    const item = document.createElement('div')
    item.className = 'source-item'
    item.textContent = `[${i + 1}] ${src}`
    list.appendChild(item)
  })

  toggle.addEventListener('click', () => {
    const open = list.classList.toggle('open')
    toggle.textContent = open
      ? `Hide sources`
      : `Show ${sources.length} sources`
  })

  wrapper.appendChild(toggle)
  wrapper.appendChild(list)
  messages.appendChild(wrapper)
  messages.scrollTop = messages.scrollHeight
}

// ── Reset ─────────────────────────────────────────────────

resetBtn.addEventListener('click', () => {
  chatHistory = []           // add this line
  messages.innerHTML = ''
  fileInput.value = ''
  uploadStatus.textContent = ''
  uploadStatus.className = 'upload-status'
  chatSection.classList.add('hidden')
  uploadSection.classList.remove('hidden')
})