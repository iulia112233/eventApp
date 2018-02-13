    let app = new Vue({
      el: '#app',
      delimiters: ['${', '}'],
      data: {
        username: '',
        link: '',
        fd:'',
      },
      methods: {
        submit: function() { 
          let fd = new FormData();
          fd.append('username', this.username);
          axios.post('/api/reset', fd)
            .then(res => {
              this.link = res.data.outcome;
              })
              .catch(err => { console.log(err); });
            }
          }
        });
