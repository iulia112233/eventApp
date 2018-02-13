    Vue.use(VeeValidate);
    root = new Vue({
      delimiters: ['${', '}'],
      el: '#app',
      data: {
        formData: {},
        labelVal: '',
        myForm: {
            username: '',
            password: '',
        },
        displayResponse: '',
        isAlert: true,
        isSuccess: false,
        hasError: false,
      },
      methods: {
        submit(){
          axios.post('/api/login', JSON.parse(JSON.stringify(this.myForm)))
          .then(res => {
          console.log(res);
          this.displayResponse = true; 
          this.isSuccess = true; 
          this.labelVal = res.data.outcome;
          window.location.href = '/index';
          } ).catch(err => { 
                this.displayResponse = true;
                this.hasError = true; 
                this.labelVal = err.response.data.outcome;
                });
         },
        validateBeforeSubmit(){
          this.$validator
            .validateAll()
            .then(function(response){
              if(response){
                this.root.submit();
                }
            })
          .catch(err =>{
            console.log(err);
          })
        }       
      }
    });
    

