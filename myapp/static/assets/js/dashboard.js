function makeSegmentPie(values){
    AmCharts.makeChart("segment-pie",
				{
					"type": "pie",
					"balloonText": "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>",
					"innerRadius": "78%",
					"labelRadius": 10,
					"titleField": "segment__title",
					"valueField": "qtd",
					"theme": "dark",
					"allLabels": [],
					"balloon": {},
					"legend": {
						"enabled": true,
						"align": "center",
						"markerType": "circle"
					},
					"titles": [
					],
					"dataProvider":values
				}
    )
};
function makePurchaseStatusLine(values){
    AmCharts.makeChart("purchase-status-line",
				{
					"type": "serial",
					"categoryField": "purchase_status__title",
					"startDuration": 1,
					"theme": "dark",
					"categoryAxis": {
						"gridPosition": "start"
					},
					"trendLines": [],
					"graphs": [
						{
							"colorField": "color",
							"fillAlphas": 1,
							"id": "AmGraph-1",
							"lineColorField": "color",
							"title": "graph 1",
							"type": "column",
							"valueField": "qtd"
						}
					],
					"guides": [],
					"valueAxes": [
						{
							"id": "ValueAxis-1",
							"title": "Quantity of Customers"
						}
					],
					"allLabels": [],
					"balloon": {},
					"titles": [],
					"dataProvider": values
				}
			);
};