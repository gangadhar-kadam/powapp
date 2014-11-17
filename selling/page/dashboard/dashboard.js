	wn.pages['dashboard'].onload = function(wrapper) { 
	wn.ui.make_app_page({
		parent: wrapper,
		title: 'Dashboard',
		single_column: true
	});	
	//$wrapper.append('<div id="select_condition">FusionCharts XT will load here!</div>')
	$('<div class="select_condition">Please Select A Criteria For Dashboard <select id="select_type" name="dropdown"><option value="cm" selected>Current Months</option><option value="all">All</option></select> </div>').appendTo($wrapper.find(".appframe"));				
    console.log($('#select_type').val());
    console.log("calling default value function");

	wn.call({
			type: "POST",
			method: "selling.utils.product.get_data",
			args: {
				   fullname: $('#select_type').val()
				},
			callback: function(r) {
				if(r.message=="No") {
						$wrapper.find("appframe container").append('<div id="message">No Data Found for selected condition....!</div>')
				
				}
				else{
					//alert(r.message);
					aa='<script type="text/javascript" src="FusionCharts/FusionCharts.js"></script><body><div id="chartContainer"></div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1250", "500", "0" );myChart.setJSONData('
	            	bb=aa+r.message+');myChart.render("chartContainer");</script></body>'
					$wrapper.append(bb)		
				}
			}
		})

$('#select_type').bind("click",function(){
   
	wn.call({
		type: "POST",
		method: "selling.utils.product.get_data",
		args: {
			   fullname: $('#select_type').val()
			},
		callback: function(r) {
			if(r.message=="No") {
					$wrapper.find("appframe container").append('<div id="message">No Data Found for selected condition....!</div>')
			
			}
			else{
				//alert(r.message);
				aa='<script type="text/javascript" src="FusionCharts/FusionCharts.js"></script><body><div id="chartContainer"></div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1250", "500", "0" );myChart.setJSONData('
            	bb=aa+r.message+');myChart.render("chartContainer");</script></body>'
				$wrapper.append(bb)		
			}
		}
	})
})

//$wrapper.append('<html><head><title>My First chart using FusionCharts XT - JSON data URL</title> <script type="text/javascript" src="FusionCharts/FusionCharts.js"></script> </head> <body><div id="chartContainer">FusionCharts XT will load here!</div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1000", "600", "0" );myChart.setJSONData( {"chart": {"caption": "Monthly Sales Summary","xAxisName": "Franchise","yAxisName": "Sales","numberPrefix": "Rs"},"data": [{"label": "franchise 1","value": "14400"},{"label": "franchise 2","value": "19600"},{"label": "franchise 3","value": "24000" },{ "label": "franchise 4","value": "700" },{ "label": "franchise 5","value": "115700"},{ "label": "franchise 6","value": "55700" }]} );myChart.render("chartContainer");</script></body></html>')
//$wrapper.append('<html><head><title>My First chart using FusionCharts XT - JSON data URL</title> <script type="text/javascript" src="FusionCharts/FusionCharts.js"></script> </head> <body><div id="chartContainer">FusionCharts XT will load here!</div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1000", "600", "0" );myChart.setJSONData( { "chart":  { "caption" : "Weekly Sales Summary" , "xAxisName" : "Week", "yAxisName" : "Sales", "numberPrefix" : "$" },"data" : [ { "label" : "Week 1", "value" : "14400" },{ "label" : "Week 2", "value" : "19600" }, { "label" : "Week 3", "value" : "24000" }, { "label" : "Week 4", "value" : "15700" } ]} );myChart.render("chartContainer");</script></body></html>')
 }
















//wn.pages['dashboard'].onload = function(wrapper) { 
//	wn.ui.make_app_page({
//		parent: wrapper,
//		title: 'Dashbaord',
//		single_column: true
//	});					
//}
//
//         wn.pages['dashboard'].onload = function(wrapper) {
//        wn.ui.make_app_page({
//                parent: wrapper,
//                title: 'dashboard',
///                single_column: true
//        });
//alert("calling server");
//wn.call({
////                type: "POST",
//                method: "selling.utils.product.get_data",
//                args: {
//                        },
//                callback: function(r) {
//                        if(r.message ) {
//                        //alert(r.message);
//                        aa='<html><head><title>My First chart using FusionCharts XT - JSON data URL</title> <script type="text/javascript" src="FusionCharts/FusionCharts.js"></script> </head> <body><div id="chartContainer">FusionCharts XT will load here!</div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1000", "520", "0" );myChart.setJSONData('
///                        bb=aa+r.message+');myChart.render("chartContainer");</script></body></html>'
//                        //alert(bb);
//                        $wrapper.append(bb)
//                        //$wrapper.find("#chartContainer").append(bb)
//
//                        }
//                        else{
//                        alert("no data found");
//                        }
//                }
//        })

//$wrapper.append('<html><head><title>My First chart using FusionCharts XT - JSON data URL</title> <script type="text/javascript" src="FusionCharts/FusionCharts.js"></script> </head> <body><div id="chartContainer">FusionCharts XT will load here!</div> <script type="text/javascript">  var myChart = new FusionCharts( "FusionCharts/Column3D.swf", "myChartId", "1000", "600", "0" );myChart.setJSONData( {"chart": {"caption": "Monthly Sales Summary","xAxisName": "Franchise","yAxisName": "Sales","numberPrefix": "Rs"},"data": [{"label": "franchise 1","value": "14400"},{"label": "franchise 2","value": "19600"},{"label": "franchise 3","value": "24000" },{ "label": "franchise 4","value": "700" },{ "label": "franchise 5","value": "115700"},{ "label": "franchise 6","value": "55700" }]} );myChart.render("chartContainer");</script></body></html>')
//}




