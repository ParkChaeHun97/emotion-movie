const express = require('express');
const router = express.Router();
const { User } = require("../models/User");

//=================================
//             Register
//=================================

router.post('/register', (req, res) => {
    const { name, email, password, lastname } = req.body;
    const user = new User({ name, email, password, lastname });
    user.save((err, user) => {
        if (err) return res.json({
            success: false,
            message: err,
        })
        return res.status(200).json({
            success: true
        })
    })
})

router.post('/checkId/:id', (req, res) => {
    User.findOne({ id: req.body.id }, (err, user) => {
        if (!user) return res.status(200).send();
        else return res.status(404).json({
            success: false
        })
    })
})

module.exports = router;