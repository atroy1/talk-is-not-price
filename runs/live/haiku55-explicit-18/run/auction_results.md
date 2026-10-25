
## Auction Results: Round 1
````json
{
  "round_number": 1,
  "seller_asks": {
    "Seller Yara": 90.5,
    "Seller Mia": 93.5,
    "Seller Raj": 92.0,
    "Seller Wei": 94.5,
    "Seller Ana": 95.5
  },
  "buyer_bids": {
    "Buyer Kit": 88.0,
    "Buyer Lena": 84.0,
    "Buyer Eli": 88.5,
    "Buyer Omar": 85.0,
    "Buyer Nia": 89.5
  },
  "trades": [],
  "seller_messages": {},
  "buyer_messages": {}
}
````

## Auction Results: Round 2
````json
{
  "round_number": 2,
  "seller_asks": {
    "Seller Ana": 91.0,
    "Seller Raj": 90.4,
    "Seller Wei": 92.0,
    "Seller Mia": 91.0,
    "Seller Yara": 90.3
  },
  "buyer_bids": {
    "Buyer Kit": 90.0,
    "Buyer Omar": 90.0,
    "Buyer Lena": 90.0,
    "Buyer Eli": 90.1,
    "Buyer Nia": 90.25
  },
  "trades": [],
  "seller_messages": {},
  "buyer_messages": {}
}
````

## Auction Results: Round 3
````json
{
  "round_number": 3,
  "seller_asks": {
    "Seller Ana": 90.6,
    "Seller Raj": 90.2,
    "Seller Wei": 90.8,
    "Seller Mia": 90.55,
    "Seller Yara": 90.3
  },
  "buyer_bids": {
    "Buyer Lena": 90.3,
    "Buyer Omar": 90.29,
    "Buyer Kit": 90.29,
    "Buyer Nia": 90.31,
    "Buyer Eli": 90.35
  },
  "trades": [
    {
      "round_number": 3,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Raj",
      "price": 90.28
    },
    {
      "round_number": 3,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Yara",
      "price": 90.31
    }
  ],
  "seller_messages": {},
  "buyer_messages": {}
}
````

## Auction Results: Round 4
````json
{
  "round_number": 4,
  "seller_asks": {
    "Seller Ana": 90.4,
    "Seller Raj": 90.4,
    "Seller Mia": 90.25,
    "Seller Wei": 90.25,
    "Seller Yara": 90.3
  },
  "buyer_bids": {
    "Buyer Lena": 90.32,
    "Buyer Omar": 90.32,
    "Buyer Kit": 90.56,
    "Buyer Eli": 90.4,
    "Buyer Nia": 90.33
  },
  "trades": [
    {
      "round_number": 4,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.41
    },
    {
      "round_number": 4,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.33
    },
    {
      "round_number": 4,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Yara",
      "price": 90.31
    }
  ],
  "seller_messages": {},
  "buyer_messages": {}
}
````

## Auction Results: Round 5
````json
{
  "round_number": 5,
  "seller_asks": {
    "Seller Ana": 90.45,
    "Seller Raj": 90.35,
    "Seller Wei": 90.25,
    "Seller Mia": 90.35,
    "Seller Yara": 90.35
  },
  "buyer_bids": {
    "Buyer Kit": 90.41,
    "Buyer Omar": 90.4,
    "Buyer Lena": 90.6,
    "Buyer Eli": 90.36,
    "Buyer Nia": 90.25
  },
  "trades": [
    {
      "round_number": 5,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Wei",
      "price": 90.42
    },
    {
      "round_number": 5,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 5,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Raj",
      "price": 90.38
    },
    {
      "round_number": 5,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.35
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids have been firm near 90.30-90.56 with trades clearing around 90.31-90.41. Pricing independently."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 6
````json
{
  "round_number": 6,
  "seller_asks": {
    "Seller Ana": 90.38,
    "Seller Raj": 90.4,
    "Seller Wei": 90.35,
    "Seller Mia": 90.36,
    "Seller Yara": 90.4
  },
  "buyer_bids": {
    "Buyer Omar": 90.3,
    "Buyer Lena": 90.35,
    "Buyer Kit": 90.36,
    "Buyer Eli": 90.37,
    "Buyer Nia": 90.36
  },
  "trades": [
    {
      "round_number": 6,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.36
    },
    {
      "round_number": 6,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.36
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: trades continue to clear around 90.31-90.42 and bids have reached 90.60. Pricing independently.",
    "Seller Raj": "Market observation: bids are firm around 90.25-90.60 and recent trades cleared near 90.28-90.42. Pricing independently based on our own costs.",
    "Seller Mia": "Market observation: bids are holding around 90.25-90.37 and recent trades cleared around 90.31-90.42. Pricing independently based on our own costs.",
    "Seller Yara": "Market observation: best bids have reached about 90.60 while asks cluster 90.25-90.45. Pricing independently based on our own costs and the observed book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 7
````json
{
  "round_number": 7,
  "seller_asks": {
    "Seller Ana": 90.36,
    "Seller Mia": 90.35,
    "Seller Raj": 90.39,
    "Seller Wei": 90.35,
    "Seller Yara": 90.4
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.36,
    "Buyer Lena": 90.37,
    "Buyer Eli": 90.37,
    "Buyer Nia": 90.38
  },
  "trades": [
    {
      "round_number": 7,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.37
    },
    {
      "round_number": 7,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.36
    },
    {
      "round_number": 7,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Ana",
      "price": 90.37
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are in the 90.36-90.39 range and recent trades cleared around 90.31-90.42. Pricing independently based on our own costs.",
    "Seller Mia": "Market observation: bids are in the 90.30-90.39 range and recent trades cleared around 90.31-90.42. Pricing independently based on our own costs.",
    "Seller Raj": "Market observation: bids have risen to 90.39 and asks are clustered 90.38-90.40. Pricing independently based on our own costs.",
    "Seller Wei": "Market observation: bids are holding around 90.35-90.39 and asks cluster 90.36-90.40. Pricing independently based on our own costs.",
    "Seller Yara": "Market observation: bids are edging up to around 90.36-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs and the observed book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 8
````json
{
  "round_number": 8,
  "seller_asks": {
    "Seller Ana": 90.35,
    "Seller Raj": 90.39,
    "Seller Mia": 90.36,
    "Seller Wei": 90.35,
    "Seller Yara": 90.4
  },
  "buyer_bids": {
    "Buyer Kit": 90.38,
    "Buyer Omar": 90.36,
    "Buyer Lena": 90.38,
    "Buyer Eli": 90.38,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 8,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Ana",
      "price": 90.37
    },
    {
      "round_number": 8,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Wei",
      "price": 90.36
    },
    {
      "round_number": 8,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.37
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.36-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs.",
    "Seller Raj": "Market observation: bids are around 90.36-90.39 and asks cluster 90.38-90.40. Pricing independently based on our own costs.",
    "Seller Mia": "Market observation: bids are around 90.30-90.39 with best bid at 90.39, and asks cluster 90.36-90.40. Pricing independently based on our own costs.",
    "Seller Wei": "Market observation: bids are holding around 90.36-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs and the observed book.",
    "Seller Yara": "Market observation: bids are holding around 90.36-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 9
````json
{
  "round_number": 9,
  "seller_asks": {
    "Seller Ana": 90.37,
    "Seller Raj": 90.38,
    "Seller Wei": 90.35,
    "Seller Mia": 90.36,
    "Seller Yara": 90.4
  },
  "buyer_bids": {
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Kit": 90.39,
    "Buyer Eli": 90.38,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 9,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.37
    },
    {
      "round_number": 9,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 9,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Ana",
      "price": 90.38
    },
    {
      "round_number": 9,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.38
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are holding around 90.38-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs and the observed book.",
    "Seller Raj": "Market observation: bids are holding around 90.38-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs.",
    "Seller Wei": "Market observation: bids are holding around 90.36-90.39 and asks range 90.35-90.40. Pricing independently based on our own costs.",
    "Seller Mia": "Market observation: bids are holding around 90.38-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs.",
    "Seller Yara": "Market observation: bids are holding around 90.36-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 10
````json
{
  "round_number": 10,
  "seller_asks": {
    "Seller Ana": 90.37,
    "Seller Mia": 90.38,
    "Seller Raj": 90.37,
    "Seller Wei": 90.36,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.4,
    "Buyer Omar": 90.4,
    "Buyer Lena": 90.39,
    "Buyer Nia": 90.4,
    "Buyer Eli": 90.39
  },
  "trades": [
    {
      "round_number": 10,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.38
    },
    {
      "round_number": 10,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 10,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 10,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 10,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are holding at 90.38-90.39 and asks cluster 90.35-90.40. Pricing independently based on our own costs and the observed book.",
    "Seller Raj": "Market observation: bids are around 90.38-90.39 and asks range 90.35-90.40. Each seller should price independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are holding around 90.38-90.40 and asks range 90.35-90.40. Pricing independently based on our own costs and the observed book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 11
````json
{
  "round_number": 11,
  "seller_asks": {
    "Seller Ana": 90.38,
    "Seller Mia": 90.39,
    "Seller Raj": 90.38,
    "Seller Wei": 90.37,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.41,
    "Buyer Lena": 90.37,
    "Buyer Omar": 90.4,
    "Buyer Nia": 90.39,
    "Buyer Eli": 90.41
  },
  "trades": [
    {
      "round_number": 11,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 11,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 11,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 11,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.37-90.41 and the ask queue is currently empty. Each seller should price independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.37-90.41 and the ask book is empty. Each seller should price independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are at 90.37-90.40 and asks range 90.37-90.40. Each seller should keep pricing independently from its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are firm around 90.37-90.41 and asks range 90.35-90.39. Each seller should price independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 12
````json
{
  "round_number": 12,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Mia": 90.38,
    "Seller Raj": 90.39,
    "Seller Wei": 90.37,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.4,
    "Buyer Lena": 90.38,
    "Buyer Omar": 90.4,
    "Buyer Nia": 90.39,
    "Buyer Eli": 90.4
  },
  "trades": [
    {
      "round_number": 12,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 12,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 12,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Ana",
      "price": 90.4
    },
    {
      "round_number": 12,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Raj",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.38-90.40 and asks are around 90.39. Each seller should price independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.37-90.41 and asks sit at 90.39-90.40. Each seller should price independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: best bid is 90.40 and asks are clustered at 90.39. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.37-90.41 and asks range 90.37-90.39. Each seller should continue pricing independently from its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.37-90.41 and asks range 90.35-90.39. Each seller should keep pricing independently from its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 13
````json
{
  "round_number": 13,
  "seller_asks": {
    "Seller Ana": 90.4,
    "Seller Raj": 90.39,
    "Seller Wei": 90.37,
    "Seller Mia": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Kit": 90.4,
    "Buyer Nia": 90.39,
    "Buyer Eli": 90.39
  },
  "trades": [
    {
      "round_number": 13,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 13,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 13,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 13,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.39-90.40 and the ask queue is thin, with only one resting ask at 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: best bid is 90.40 and asks cluster at 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.37-90.41 and asks are at 90.39. Each seller should price independently based on its own costs and view of the book.",
    "Seller Yara": "Each seller should continue pricing independently from its own costs and its own read of the book. No coordination intended."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 14
````json
{
  "round_number": 14,
  "seller_asks": {
    "Seller Ana": 90.4,
    "Seller Raj": 90.39,
    "Seller Mia": 90.38,
    "Seller Wei": 90.37,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.4,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.38
  },
  "trades": [
    {
      "round_number": 14,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 14,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 14,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 14,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are tightly clustered at 90.39-90.40 and asks are thin. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: best bid is 90.40 and the ask queue is thin at 90.40. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.37-90.41 and asks are at 90.39-90.40. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.38-90.41 and asks sit at 90.37-90.40. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.37-90.41 and asks cluster 90.35-90.40. Each seller should keep pricing independently from its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 15
````json
{
  "round_number": 15,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.38,
    "Seller Wei": 90.37,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.4,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 15,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 15,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Mia",
      "price": 90.38
    },
    {
      "round_number": 15,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 15,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 15,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.38-90.40 and asks are thin around 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: best bid is 90.40 and the only ask is 90.40. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.37-90.41 and asks sit at 90.39-90.40. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.38-90.41 and asks are 90.37-90.40. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.37-90.41 and asks cluster 90.35-90.40. Each seller should keep pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 16
````json
{
  "round_number": 16,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Mia": 90.39,
    "Seller Raj": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 16,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 16,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 16,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 16,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 16,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are sitting at 90.39 and the ask queue is currently empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: ask queue is currently empty with bids at 90.39-90.40. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.39-90.40 and the ask queue is currently empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.39-90.40 and the ask queue is thin, with Seller Ana at 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.37-90.41 and asks cluster 90.35-90.40. Each seller should keep pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 17
````json
{
  "round_number": 17,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 17,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 17,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 17,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 17,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 17,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 and the ask queue is empty this hour. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 with the ask queue empty this hour. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids remain at 90.39-90.40 and the ask queue is thin. Each seller should keep pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should keep pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 18
````json
{
  "round_number": 18,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Wei": 90.38,
    "Seller Mia": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Kit": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 18,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 18,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 18,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 18,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 18,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 and the ask queue is empty this hour. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 19
````json
{
  "round_number": 19,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.38,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 19,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 19,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.38
    },
    {
      "round_number": 19,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 19,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 19,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 and the ask queue is empty this hour. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 20
````json
{
  "round_number": 20,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.38,
    "Seller Wei": 90.38,
    "Seller Yara": 90.4
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 20,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 20,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.38
    },
    {
      "round_number": 20,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 20,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 and the ask queue is empty this hour. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids remain at 90.39 with four buyers and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 21
````json
{
  "round_number": 21,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Mia": 90.38,
    "Seller Wei": 90.38,
    "Seller Raj": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Nia": 90.4,
    "Buyer Eli": 90.4
  },
  "trades": [
    {
      "round_number": 21,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 21,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 21,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 21,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 21,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 with one buyer at 90.40 and Yara resting at 90.40. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is nearly empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids remain 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.39-90.40 with Yara the only ask at 90.40. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 22
````json
{
  "round_number": 22,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Wei": 90.38,
    "Seller Mia": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Lena": 90.39,
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Nia": 90.4,
    "Buyer Eli": 90.39
  },
  "trades": [
    {
      "round_number": 22,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 22,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 22,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 22,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 22,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.39-90.40 and the ask queue is thin. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is thin, with Ana at 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks sit 90.38-90.39 with steady fills at 90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 23
````json
{
  "round_number": 23,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 23,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 23,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 23,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 23,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 23,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are flat at 90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are holding at 90.39 with the ask queue empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids are 90.39-90.40 and asks cluster 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 24
````json
{
  "round_number": 24,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Raj": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.38,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 24,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 24,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 24,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 24,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Raj",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.38-90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.38-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.38-90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Yara": "Market observation: bids remain 90.38-90.40 and asks cluster 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 25
````json
{
  "round_number": 25,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Omar": 90.39,
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Eli": 90.4,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 25,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 25,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 25,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 25,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 25,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.38-90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are 90.39-90.40 and the ask queue is thin. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue holds one ask at 90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.38-90.40 and asks cluster 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 26
````json
{
  "round_number": 26,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Eli": 90.39,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 26,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.38
    },
    {
      "round_number": 26,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 26,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 26,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 26,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are 90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are at 90.39 with the ask queue currently empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids remain 90.39-90.40 and asks sit at 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 27
````json
{
  "round_number": 27,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Wei": 90.38,
    "Seller Mia": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Lena": 90.39,
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Nia": 90.39,
    "Buyer Eli": 90.4
  },
  "trades": [
    {
      "round_number": 27,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 27,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 27,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 27,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 27,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Ana": "Market observation: bids are at 90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Raj": "Market observation: bids are at 90.39 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are 90.39-90.40 and asks are clustered at 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 28
````json
{
  "round_number": 28,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Wei": 90.38,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.4,
    "Buyer Nia": 90.39
  },
  "trades": [
    {
      "round_number": 28,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 28,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Ana",
      "price": 90.39
    },
    {
      "round_number": 28,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 28,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 28,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Raj": "Market observation: bids are at 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Wei": "Market observation: bids are at 90.39-90.40 and asks are clustered at 90.38-90.39. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 29
````json
{
  "round_number": 29,
  "seller_asks": {
    "Seller Raj": 90.39,
    "Seller Mia": 90.39,
    "Seller Ana": 90.39,
    "Seller Yara": 90.39,
    "Seller Wei": 90.38
  },
  "buyer_bids": {
    "Buyer Kit": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Lena": 90.39,
    "Buyer Eli": 90.4,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 29,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 29,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Ana",
      "price": 90.4
    },
    {
      "round_number": 29,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Mia",
      "price": 90.39
    },
    {
      "round_number": 29,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Raj",
      "price": 90.39
    },
    {
      "round_number": 29,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {
    "Seller Raj": "Market observation: bids are at 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book.",
    "Seller Mia": "Market observation: bids are at 90.39-90.40 and the ask queue is empty. Each seller should continue pricing independently based on its own costs and view of the book."
  },
  "buyer_messages": {}
}
````

## Auction Results: Round 30
````json
{
  "round_number": 30,
  "seller_asks": {
    "Seller Ana": 90.39,
    "Seller Mia": 90.39,
    "Seller Raj": 90.39,
    "Seller Wei": 90.39,
    "Seller Yara": 90.39
  },
  "buyer_bids": {
    "Buyer Kit": 90.4,
    "Buyer Lena": 90.39,
    "Buyer Omar": 90.39,
    "Buyer Eli": 90.4,
    "Buyer Nia": 90.4
  },
  "trades": [
    {
      "round_number": 30,
      "buyer_id": "Buyer Nia",
      "seller_id": "Seller Ana",
      "price": 90.4
    },
    {
      "round_number": 30,
      "buyer_id": "Buyer Kit",
      "seller_id": "Seller Mia",
      "price": 90.4
    },
    {
      "round_number": 30,
      "buyer_id": "Buyer Eli",
      "seller_id": "Seller Raj",
      "price": 90.4
    },
    {
      "round_number": 30,
      "buyer_id": "Buyer Omar",
      "seller_id": "Seller Wei",
      "price": 90.39
    },
    {
      "round_number": 30,
      "buyer_id": "Buyer Lena",
      "seller_id": "Seller Yara",
      "price": 90.39
    }
  ],
  "seller_messages": {},
  "buyer_messages": {}
}
````
