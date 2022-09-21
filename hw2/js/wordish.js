"use strict"

let guess_count = 0

function start(){
    console.log("I'm here")
    let target = document.getElementById("target_text").value
    if (target.length != 5) {
        document.getElementById('status').innerHTML = "invalid input"
        return
    }
    for (let i = 0; i < 5; i++) {
        let x = target.substring(i, i + 1)
        if (x < 'a' || x > 'z') {
            document.getElementById('status').innerHTML = `invalid input`
            return
        }
    }
    document.getElementById("status").innerHTML = "start"
}

function guess() {
    document.getElementById("status").innerHTML = "good guess"
    let target = document.getElementById("target_text").value
    let word = document.getElementById("guess_text").value
    let win = false
    if (word === target) {
        win = true
    }
    
    if (word.length != 5) {
        document.getElementById('status').innerHTML = "invalid input"
        return
    }
    for (let i = 0; i < 5; i++) {
        let x = word.substring(i, i + 1)
        if (x < 'a' || x > 'z') {
            document.getElementById('status').innerHTML = `invalid input`
            return
        }
    }

    for (let i = 0; i < 5; i++) {
        let x = word.substring(i, i + 1)
        let y = target.substring(i, i + 1)
        let cell = document.getElementById("cell_" + guess_count + "_" + i)
        cell.innerHTML = x
        cell.style.backgroundColor = "gray"
        if (x === y) {
            cell.style.backgroundColor = "green"
            target = target.substring(0, i) + "-" + target.substring(i + 1)
        }
    }

    for (let i = 0; i  < 5; i++) {
        let x = word.substring(i, i + 1)
        let idx = target.indexOf(x)
        let cell = document.getElementById("cell_" + guess_count + "_" + i)
        if ((idx !== -1) && (cell.style.backgroundColor !== "green")) {
            cell.style.backgroundColor = "yellow"
            target = target.substring(0, idx) + "-" + target.substring(idx + 1)
        }
    }

    if (win){
        document.getElementById('status').innerHTML = "win"
        return
    }

    guess_count++
    if (guess_count === 6) {
        document.getElementById('status').innerHTML = "lose"
    }
}