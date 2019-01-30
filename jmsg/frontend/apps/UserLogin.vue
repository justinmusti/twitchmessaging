<template>
    <div>
        <h4>Login</h4>
        <div v-if="error" class="ui warning message">
            <div class="header">
                {{error}}
            </div>
        </div>
        <form action="javascript:void(0);" method="POST" class="ui form" v-bind:class="{loading:isProcessing}">
            <div class="field">
                <label>Username</label>
                <input type="text" v-model="username" name="username" placeholder="Username"/>
            </div>

            <div class="field">
                <label>Password</label>
                <input type="password" v-model="password" name="password" placeholder="Password"/>
            </div>

            <div class="field">
                <input class="ui primary fluid button" v-on:click="submit" type="submit" name="submit" value="Login">
            </div>
        </form>
    </div>
</template>

<script>

    export default {

        props: {
            login_url: {required: true}
        },

        data() {
            return {
                error: '',
                username: '',
                password: '',
                isProcessing: false
            }
        },

        methods: {

            submit: function(){
                this.isProcessing = true;
                if(!this.username){
                    this.error = 'Must provide a username';
                    this.isProcessing = false;
                    return
                }
                if (!this.password) {
                    this.error = 'Must provide a password';
                    this.isProcessing = false;
                    return
                }
                this.error = '';

                fetch(this.login_url, {
                    method: 'POST',
                    body: JSON.stringify({username: this.username, password: this.password}),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(res => res.json())
                    .then(response => {

                        console.log("Response", response);
                        if(!response.status){
                            this.error = response.error
                        } else{
                            //Everything is good, Send user home.
                            window.location.href = '/';

                        }
                        this.isProcessing = false;
                    })
                    .catch(error => {console.error('Error:', error);
                        this.isProcessing = false;});
            }

        }
    }

    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }


</script>