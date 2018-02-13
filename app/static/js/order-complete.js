    var app = new Vue ({
        el: '#app',
        delimiters: ['${', '}'],
        data: {
            orderDetails: false
        },
        created(){
            
            var arr = document.URL.match(/(charge_id=)([a-z])\w(_)([0-9])([A-Z])\w+/)
            var charge_id = arr[0].split('=')[1];
            
            axios.post('/api/order-completed', {'charge_id': charge_id})
                .then((res)=>{
                  this.orderDetails = res.data.charge;
                  this.orderDetails.currency = this.orderDetails.currency.toUpperCase();
            });
        },
        filters: {
          moment(date) {
            return moment.unix(date).format('MMMM Do, YYYY - h:mm a');
        },
         currency(amount){
          return `${(amount/100).toFixed( 2 )}`;
       }
    }
     });

