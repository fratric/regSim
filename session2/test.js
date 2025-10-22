console.log("Example of screening wallet address explicitly using Circle's API");

import axios from 'axios'

const options = {
  method: 'POST',
  url: 'https://api.circle.com/v1/w3s/compliance/screening/addresses',
  headers: {
    Authorization: 'Bearer TEST_API_KEY:6134d1301cb8efa367632fe0d59a8852:16db8684eadd8b7e412cf67809ef963a',
    'Content-Type': 'application/json',
  },
  data: {
    idempotencyKey: '44bd2d89-9461-4502-84ba-550c9e278db7', // unique-idempotency-key
    address: '0x33314ad8Cfd12Becb448B4Aaf4d5aE4Ca87e9999',
    chain: 'ETH-SEPOLIA',
  },
}

axios
  .request(options)
  .then(function (response) {
    console.log(response.data)
    console.log("Suggested Actions: " + response.data.data.decision.actions)
  })
  .catch(function (error) {
    console.error(error)
  })