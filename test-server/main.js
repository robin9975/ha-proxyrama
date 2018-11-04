const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => res.send('Hello World!'))
app.get('/notfound', (req, res) => {
	res.status(404);
	throw new Error("Not found");
})
app.get('/error', (req, res) => {
	throw new Error("Invalid server error")
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
