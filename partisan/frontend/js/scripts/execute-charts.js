import {Charter} from '../libraries/charter.js';

Charter.createSentimentPieChart(
  'politics-sentiment',
  'This is my Chart Title!',
  [
    {
      'label': 'Positive',
      'value': 30
    },
    {
      'label': 'Negative',
      'value': 20
    },
    {
      'label': 'Neutral',
      'value': 50
    }
  ]
);
