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
                        v-on:click="fetchMessages(contact.id)"
                    >
                        {{ capitalizeFirstLetter(contact.username) }}
                    </a>
                </div>


            </div>
            <div class="eight wide column">
                <div class="in-page-message-cover">
                    <div class="ui list">
                        <div class="item">Message1</div>
                        <div class="item">Message2</div>
                        <div class="item">Message3</div>
                        <div class="item">Message4</div>
                        <div class="item">Message5</div>
                        <div class="item">{{contacts_list_url}}</div>
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
                contact_list: []
            }
        },

        methods: {
          fetchMessages: function(userId){
              console.log('I am fired', userId )
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


</script>