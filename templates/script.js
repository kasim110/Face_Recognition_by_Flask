let broker = document.getElementById('refer-btn');
let brokerShow = document.getElementById('gform_63');
let borrower = document.getElementById('finance-btn');
let borrowerShow = document.getElementById('gform_7');

borrower.addEventListener('click', function() {
    if(borrowerShow.style.display == 'block') {
      borrowerShow.style.display = 'none';
      
    }else {
      borrowerShow.style.display = 'block';
      brokerShow.style.display = 'none';
    }
  }, false);


broker.addEventListener('click', function() {
    if(brokerShow.style.display == 'block') {
      brokerShow.style.display = 'none';
      
    }else {
      brokerShow.style.display = 'block';
      borrowerShow.style.display = 'none';
    }
  }, false);