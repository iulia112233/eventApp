var arr = document.URL.match(/id=([0-9]+)/)
var id = arr[1];
 
 var app = new Vue({
      el: "#app",
      delimiters: ["${", "}"],
      data: {
        
            stripeKey: 'pk_test_c9A05XZrxznbqyFQz3iVSm9R',

            // fields
            name: 'Connor Leech',
            email: 'connor@employbl.com',
            engravingText: 'This is the text to put on the bundle of sticks',
            address: {
                street: '123 Something Lane',
                city: 'San Francisco',
                state: 'CA',
                zip: '94607'
            },
            amount: 0,
            currency: '',
            type: '',
            card: {
                number: '4242424242424242',
                cvc: '123',
                exp_month: '01',
                exp_year: '19'
            },

            // validation
            cardNumberError: null,
            cardCvcError: null,
            cardMonthError: null,
            cardYearError: null,
            cardCheckSending: false,
            cardCheckError: false,
            cardCheckErrorMessage: ''
        
    },
    created() {
      let fd = new FormData();
      fd.append('id', id);

      axios.post('/api/loadTicketData', fd)
        .then(res => {
          console.log(res);
            this.name = res.data[0].surname + ' '+  res.data[0].name;
            this.email = 'iulia@phyramid.com';
            this.engravingText  = 'Tickets for ' + res.data[0].eventTitle;
            this.amount = res.data[0].price;
            this.currency = res.data[0].currency;
            this.type = res.data[0].type;
          }).catch(e => {
                console.log(e);
                });

    },
    methods: {
        validate(){
            this.clearCardErrors();
            let valid = true;
            if(!this.card.number){ valid = false; this.cardNumberError = "Card Number is Required"; }
            if(!this.card.cvc){ valid = false; this.cardCvcError = "CVC is Required"; }
            if(!this.card.exp_month){ valid = false; this.cardMonthError = "Month is Required"; }
            if(!this.card.exp_year){ valid = false; this.cardYearError = "Year is Required"; }
            if(valid){
                this.createToken();
            }
        },
        clearCardErrors(){
            this.cardNumberError = null;
            this.cardCvcError = null;
            this.cardMonthError = null;
            this.cardYearError = null;
        },
        createToken() {
            this.cardCheckError = false;
            window.Stripe.setPublishableKey(this.stripeKey);
            window.Stripe.createToken(this.card, $.proxy(this.stripeResponseHandler, this));
            this.cardCheckSending = true;
        },
        stripeResponseHandler(status, response) {
            this.cardCheckSending = false;
            if (response.error) {
                this.cardCheckErrorMessage = response.error.message;
                this.cardCheckError = true;

                console.error(response.error);
            } else {
                var token_from_stripe = response.id;
                var request = {
                    name: this.name,
                    email: this.email,
                    engravingText: this.engravingText,
                    amount: this.amount * 100,
                    currency: this.currency,
                    address: this.address,
                    card: this.card,
                    token_from_stripe: token_from_stripe
                };

                axios.post('/api/charge', request)
                    .then((res) => {
                        var error = res.data.error;
                        var charge = res.data.charge;
                        console.log(res);
                        if (error){
                            console.error(error);
                        } else {
                            window.location.href = '/order-complete?charge_id='+ charge.id; 
                        }
                    });
               }
           }
         }
      });


