 Vue.use(VeeValidate);
    var app = new Vue({
      el: "#app",
      delimiters: ['${', '}'],
      data: {
        password: '',
        hasError: '',
        isAlert: '',
        isSuccess: '',
        outcome: '',
      },
      methods: {
        submit: function () {
          fd = new FormData();
          var u = document.getElementById('username');
          fd.append('username', u.value);
          fd.append('password', this.password);
          let self = this;
          
         axios.post('/api/resetPassword', fd)
           .then(res => { 
            console.log(res);
            self.isSuccess = true;
            self.outcome = res.data.outcome;
           })
             .catch(err => { console.log(err);});
          },
        validateBeforeSubmit: function () {
          let self = this;
            this.$validator
            .validateAll()
            .then(function(response){
              if(response){
                self.submit();
                }
            })
          .catch(function(){
          })

          }
        }
        });
