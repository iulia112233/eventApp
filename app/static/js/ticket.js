 Vue.component('ticket', {
      template: '#ticket-template',
      delimiters: ['${', '}'],
      props: ['remove', 'save'],
      data: function() {
        return {
          type: '',
          price: '',
          currency: '',
        }
      },
      methods: {
        removeTicket: function() {
          this.$emit('remove');
        },
        saveTicket: function(){
          this.$emit('save', this.type, this.price, this.currency);
        }
      }
   });


