<template>
    <div class="ui grid">
        <div class="row" v-if="error">
            <div class="sixteen wide column">
                <div class="ui negative message">
                    <div class="header">
                        {{error}}
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="four wide column">
                <div class="ui vertical inverted pointing menu">
                    <a class="item" v-for="contact in contact_list"
                        v-on:click="fetchConvo(contact.id)"
                    >
                        {{ capitalizeFirstLetter(contact.username) }}
                    </a>
                </div>
            </div>
            <div class="eight wide column">
                <div class="in-page-message-cover">

                    <div v-if="!conversationId" >
                        Select a user to start talking.
                    </div>
                    <div v-if="conversationId" class="ui comments">
                        <h3 class="ui dividing header">Messages</h3>
                        <div class="comment" v-for="msg in messages">

                            <div class="content">
                                <a class="author">{{capitalizeFirstLetter(msg.sender_username)}}</a>
                                <div class="text">
                                    {{msg.text}}
                                </div>
                                <div class="metadata">
                                    <span class="date">{{msg.created_at}}</span>
                                </div>
                            </div>
                        </div>


                        <form class="ui reply form" v-on:submit.prevent="sendMessage(conversationId)">
                            <div class="field">
                                <input v-model="message" type="text" placeholder="Type your message here"/>
                                Message: {{message}}
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

    export default {
        props: {
            contacts_list_url: {required: true}
        },

        data() {
            return {
                error: '',
                conversationId: '',
                contact_list: [],
                messages: '',
                message: ''
            }
        },

        methods: {
            fetchConvo: function (userId) {
                fetch('/user/conversation/' + userId + '/', {
                    method: 'GET',
                }).then(response => response.json())
                    .then(response => {
                        if (!response.status) {
                            this.error = response.error;
                            return;
                        }
                        // get messages using convo id
                        this.conversationId = response.data.conversation_id;
                        return this.fetchMessages(response.data.conversation_id)
                    })
            },

            fetchMessages: function(conversationId){
                fetch('/user/messages/' + conversationId + '/', {
                    method: 'GET',
                }).then(response => response.json())
                    .then(response => {
                        if (!response.status){
                            this.error = response.error;
                            return
                        }
                        this.messages = response.data.messages;
                    })
            },

            sendMessage: function(conversationId){
                fetch('/user/message/' + conversationId + '/', {
                    method: 'POST',
                    body: JSON.stringify({message: this.message}),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => response.json())
                    .then(response => {
                        if(!response.status){
                            this.error = response.error;
                            return;
                        }
                        this.message = '';
                        this.messages.push(response.data.message);
                    })
            },

            capitalizeFirstLetter: function (string) {
                return string.charAt(0).toUpperCase() + string.slice(1);
            }
        },

        mounted(){
            fetch(this.contacts_list_url, {
                method: 'GET',
            }).then(response => response.json())
                .then(response => {
                    if (!response.status){
                        this.error = response.error
                    }else{
                        this.contact_list = response.data
                    }

                })

        }
    }

    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

</script>