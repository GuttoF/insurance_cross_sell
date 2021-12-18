function onOpen() {
  var ui = SpreadsheetApp.getUi()
  ui.creatMenu('API Predictions').addItem('Get score', 'predictAll').addToUi()
};


function APICall(data) {
  endpoint = 'https://cross-sell-bot.herokuapp.com/predict'

  var payload = JSON.stringify(data)
  var options = {'method':'POST', 'contentType':'application/json', 'payload':payload}

  var response = UrlFetchApp.fetch(endpoint, options);

  var rc = response.getResponseCode();
  var responseText = response.getContentText();

  if (rc !== 200){
      Logger.log(response.getResponseCode())
  }
  else{
      prediction = JSON.parse(responseText)
  }
  return prediction
};


function predictAll() {
  var ss = SpreadsheetApp.getActiveSheet();
  var columns = ss.getRange('A1:L1').getValues()[0];
  var lastRow = ss.getLastRow();

  var data = ss.getRange('A2'+':'+'L'+lastRow).getValues();

  for (row in data) {
      var json = new Object;
      var json_send = new Object();

  for (j=0;j<columns.length;j++){
      json[columns[j]] = data[row][j]
  }

  json_send['id'] = json['id']
  json_send['gender'] = json['gender']
  json_send['age'] = json['age']
  json_send['driving_license'] = json['driving_license']
  json_send['region_code'] = json['region_code']
  json_send['previously_insured'] = json['previously_insured']
  json_send['vehicle_age'] = json['vehicle_age']
  json_send['vehicle_damage'] = json['vehicle_damage']
  json_send['annual_premium'] = json['annual_premium']
  json_send['policy_sales_channel'] = json['policy_sales_channel']
  json_send['vintage'] = json['vintage']
  json_send['response'] = json['response']

  prediction = APICall(json_send)

  ss.getRange(Number(row)+2, 13).setValue(prediction[0]['score']*100)
  };
};