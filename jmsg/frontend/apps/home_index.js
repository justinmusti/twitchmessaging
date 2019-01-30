import Vue from 'vue';

console.log('I am here');
var app = new Vue({
    el: '#appVue',
    data: {
        message: 'Hello Vue!'
    },

    mounted(){
        console.log('I am mounted')
    }
});