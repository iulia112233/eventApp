
    Vue.use(VeeValidate);
    root = new Vue({
      delimiters: ['${', '}'],
      el: '#app',
      data: {
        formData: {},
        labelVal: '',
        myForm: {
            username: '',
            surname: '',
            name: '',
            password: '',
            repeat:'',
            role:'guest',
        },
        displayResponse: '',
        isAlert: true,
        isSuccess: false,
        hasError: false,
        user: false,
        guest: false,
       },
      methods: {
        submit(){
        var formData = new FormData();
        formData.append('username', this.myForm.username);
        formData.append('surname', this.myForm.surname);
        formData.append('name', this.myForm.name);
        formData.append('password', this.myForm.password);
        formData.append('role',this. myForm.role);
          axios.post('/api/register', formData)
          .then(res => {
            this.displayResponse = true; 
            this.isSuccess = true;
            this.labelVal = res.data.outcome;
            window.location.href= '/index';
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
                console.log('submit');
                this.root.submit();
                }
            })
          .catch(function(){
          })
        }       
      }
    });

