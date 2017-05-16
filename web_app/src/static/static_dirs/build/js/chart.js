function rft_date_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#BDC3C7", "#26B99A", "#34495E", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#rolldown_date_wise").length) {
            var b =
echarts.init(document.getElementById("rolldown_date_wise"), a);
            b.setOption({
                title: {
                    text: data.rolldown.info,
                    // subtext: "Tractors"
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
					x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        },
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Rolldown RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.rolldown.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.rolldown.no_of_tractors,
                    
                    markPoint: {
                        data: data.rolldown.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.rolldown.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.rolldown.not_ok,
                }]
            })
        }
        if ($("#final_date_wise").length) {
            var b =
echarts.init(document.getElementById("final_date_wise"), a);
            b.setOption({
                title: {
                    text: data.final.info,
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
                    x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        },
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Final RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.final.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.final.no_of_tractors,

                    markPoint: {
                        data: data.final.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.final.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.final.not_ok,
                }]
            })
        }
        if ($("#overall_date_wise").length) {
            var b =
echarts.init(document.getElementById("overall_date_wise"), a);
            b.setOption({
                title: {
                    text: data.overall.info,
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
					x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        },
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Overall RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.overall.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.overall.no_of_tractors,

                    markPoint: {
                        data: data.overall.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.overall.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.overall.not_ok,
                }]
            })
        }
}
}

function rolldown_filter_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#BDC3C7", "#26B99A", "#34495E", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#rolldown_filter_wise").length) {
            var b =
echarts.init(document.getElementById("rolldown_filter_wise"), a);
            b.setOption({
                title: {
                    text: data.info
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
					x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        }, 
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Rolldown RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        }, 
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.no_of_tractors,

                    markPoint: {
                        data: data.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.not_ok,
                }]
            })
        }
}
}

function final_filter_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#BDC3C7", "#26B99A", "#34495E", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#final_filter_wise").length) {
            var b =
echarts.init(document.getElementById("final_filter_wise"), a);
            b.setOption({
                title: {
                    text: data.info
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
                    x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        }, 
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Final RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        }, 
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.no_of_tractors,

                    markPoint: {
                        data: data.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.not_ok,
                }]
            })
        }
}
}

function overall_filter_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#BDC3C7", "#26B99A", "#34495E", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#overall_filter_wise").length) {
            var b =
echarts.init(document.getElementById("overall_filter_wise"), a);
            b.setOption({
                title: {
                    text: data.info
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["No. of Tractors", "RFT OK", "RFT NOT OK"],
                    x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "tiled"]
                        }, 
                        dataView: {
                            show: !0,
                            title: "Table View",
                            lang: ["Final RFT", "Close", "Refresh"],
                            readOnly: !0,
                            optionToContent: function(opt) {
                                var axisData = opt.xAxis[0].data;
                                var series = opt.series;
                                var table = '<div style="position: relative; overflow: auto; width: 100%; height: 230px; cursor: default;"><table class="table table-striped"><thead><tr>'
                                             + '<th>Date</th>'
                                             + '<th>' + series[0].name + '</th>'
                                             + '<th>' + series[1].name + '</th>'
                                             + '<th>' + series[2].name + '</th>'
                                             + '</tr></thead><tbody>';
                                for (var i = 0, l = axisData.length; i < l; i++) {
                                    table += '<tr>'
                                             + '<td>' + axisData[i] + '</td>'
                                             + '<td>' + series[0].data[i] + '</td>'
                                             + '<td>' + series[1].data[i] + '</td>'
                                             + '<td>' + series[2].data[i] + '</td>'
                                             + '</tr>';
                                }
                                table += '</tbody></table></div>';
                                return table;
                            }
                        }, 
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    name: "Date",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value",
                    name: "No. of Tractors"
                }],
                
                series: [{
                    name: "No. of Tractors",
                    type: "line",
                    data: data.no_of_tractors,

                    markPoint: {
                        data: data.mark_data
                    },
                }, {
                    name: "RFT OK",
                    type: "bar",
                    stack: true,
                    data: data.rft_ok,
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    stack: true,
                    data: data.not_ok,
                }]
            })
        }
}
}


function final_model_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#26B99A", "#34495E", "#BDC3C7", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#final_filter_wise").length) {
            var b =
echarts.init(document.getElementById("final_filter_wise"), a);
            b.setOption({
                title: {
                    text: data.info,
                    subtext: "Tractors"
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["RFT OK", "RFT NOT OK"],
                    x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                stack: "Stack",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "stack", "tiled"]
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                // dataZoom : {
                //     show : true,
                //     realtime : true,
                //     start : 0,
                //     end : 100
                // },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value"
                }],
                stack: true,
                series: [{
                    name: "RFT OK",
                    type: "bar",
                    data: data.rft_ok,
                    // markPoint: {
                    //     data: [{
                    //         type: "max",
                    //         name: "???"
                    //     }, {
                    //         type: "min",
                    //         name: "???"
                    //     }]
                    // },
                    markPoint: {
                        data: data.mark_data
                    },
                    // markPoint: {
                    //     data: [{
                    //         name: "RFT OK",
                    //         value: 182.2,
                    //         xAxis: 7,
                    //         yAxis: 183
                    //     }, {
                    //         name: "RFT NOT OK",
                    //         value: 2.3,
                    //         xAxis: 11,
                    //         yAxis: 3
                    //     }]
                    // },
                    // markLine: {
                    //     data: [{
                    //         type: "average",
                    //         name: "???"
                    //     }]
                    // }
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    data: data.not_ok,

                    // markPoint: {
                    //     data: [{
                    //         type: "max",
                    //         name: "???"
                    //     }, {
                    //         type: "min",
                    //         name: "???"
                    //     }]
                    // },
                    // markLine: {
                    //     data: [{
                    //         type: "average",
                    //         name: "???"
                    //     }]
                    // }
                }]
            })
        }
}
}

function overall_model_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#26B99A", "#34495E", "#BDC3C7", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#overall_model_wise").length) {
            var b =
echarts.init(document.getElementById("overall_model_wise"), a);
            b.setOption({
                title: {
                    text: data.info,
                    subtext: "Tractors"
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    data: ["RFT OK", "RFT NOT OK"],
                    x: 'right'
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                stack: "Stack",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "stack", "tiled"]
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                // dataZoom : {
                //     show : true,
                //     realtime : true,
                //     start : 0,
                //     end : 100
                // },
                calculable: !1,
                xAxis: [{
                    type: "category",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value"
                }],
                stack: true,
                series: [{
                    name: "RFT OK",
                    type: "bar",
                    data: data.rft_ok,
                    markPoint: {
                        data: data.mark_data
                    },
                    // markPoint: {
                    //     data: [{
                    //         type: "max",
                    //         name: "???"
                    //     }, {
                    //         type: "min",
                    //         name: "???"
                    //     }]
                    // },
                    // markPoint: {
                    //     data: [{
                    //         name: "RFT OK",
                    //         value: 182.2,
                    //         xAxis: 7,
                    //         yAxis: 183
                    //     }, {
                    //         name: "RFT NOT OK",
                    //         value: 2.3,
                    //         xAxis: 11,
                    //         yAxis: 3
                    //     }]
                    // },
                    // markLine: {
                    //     data: [{
                    //         type: "average",
                    //         name: "???"
                    //     }]
                    // }
                }, {
                    name: "RFT NOT OK",
                    type: "bar",
                    data: data.not_ok,

                    // markPoint: {
                    //     data: [{
                    //         type: "max",
                    //         name: "???"
                    //     }, {
                    //         type: "min",
                    //         name: "???"
                    //     }]
                    // },
                    // markLine: {
                    //     data: [{
                    //         type: "average",
                    //         name: "???"
                    //     }]
                    // }
                }]
            })
        }
}
}


function dpu_date_wise_charts(data){
    if ("undefined" != typeof echarts) {
        console.log("init_echarts");
        var a = {
            color: ["#26B99A", "#34495E", "#BDC3C7", "#3498DB",
"#9B59B6", "#8abb6f", "#759c6a", "#bfd3b7"],
            title: {
                itemGap: 8,
                textStyle: {
                    fontWeight: "normal",
                    color: "#408829"
                }
            },
            dataRange: {
                color: ["#1f610a", "#97b58d"]
            },
            toolbox: {
                color: ["#408829", "#408829", "#408829", "#408829"]
            },
            tooltip: {
                backgroundColor: "rgba(0,0,0,0.5)",
                axisPointer: {
                    type: "line",
                    lineStyle: {
                        color: "#408829",
                        type: "dashed"
                    },
                    crossStyle: {
                        color: "#408829"
                    },
                    shadowStyle: {
                        color: "rgba(200,200,200,0.3)"
                    }
                }
            },
            dataZoom: {
                dataBackgroundColor: "#eee",
                fillerColor: "rgba(64,136,41,0.2)",
                handleColor: "#408829"
            },
            grid: {
                borderWidth: 0
            },
            categoryAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            valueAxis: {
                axisLine: {
                    lineStyle: {
                        color: "#408829"
                    }
                },
                splitArea: {
                    show: !0,
                    areaStyle: {
                        color: ["rgba(250,250,250,0.1)",
"rgba(200,200,200,0.1)"]
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: ["#eee"]
                    }
                }
            },
            timeline: {
                lineStyle: {
                    color: "#408829"
                },
                controlStyle: {
                    normal: {
                        color: "#408829"
                    },
                    emphasis: {
                        color: "#408829"
                    }
                }
            },
            k: {
                itemStyle: {
                    normal: {
                        color: "#68a54a",
                        color0: "#a9cba2",
                        lineStyle: {
                            width: 1,
                            color: "#408829",
                            color0: "#86b379"
                        }
                    }
                }
            },
            map: {
                itemStyle: {
                    normal: {
                        areaStyle: {
                            color: "#ddd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    },
                    emphasis: {
                        areaStyle: {
                            color: "#99d2dd"
                        },
                        label: {
                            textStyle: {
                                color: "#c12e34"
                            }
                        }
                    }
                }
            },
            force: {
                itemStyle: {
                    normal: {
                        linkStyle: {
                            strokeColor: "#408829"
                        }
                    }
                }
            },
            chord: {
                padding: 4,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    },
                    emphasis: {
                        lineStyle: {
                            width: 1,
                            color: "rgba(128, 128, 128, 0.5)"
                        },
                        chordStyle: {
                            lineStyle: {
                                width: 1,
                                color: "rgba(128, 128, 128, 0.5)"
                            }
                        }
                    }
                }
            },
            gauge: {
                startAngle: 225,
                endAngle: -45,
                axisLine: {
                    show: !0,
                    lineStyle: {
                        color: [
                            [.2, "#86b379"],
                            [.8, "#68a54a"],
                            [1, "#408829"]
                        ],
                        width: 8
                    }
                },
                axisTick: {
                    splitNumber: 10,
                    length: 12,
                    lineStyle: {
                        color: "auto"
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "auto"
                    }
                },
                splitLine: {
                    length: 18,
                    lineStyle: {
                        color: "auto"
                    }
                },
                pointer: {
                    length: "90%",
                    color: "auto"
                },
                title: {
                    textStyle: {
                        color: "#333"
                    }
                },
                detail: {
                    textStyle: {
                        color: "auto"
                    }
                }
            },
            textStyle: {
                fontFamily: "Arial, Verdana, sans-serif"
            }
        };
        if ($("#dpu_date_wise").length) {
            var f = echarts.init(document.getElementById("dpu_date_wise"), a);
            f.setOption({
                title: {
                    text: "Defects Per Unit",
                    subtext: "Value"
                },
                tooltip: {
                    trigger: "axis"
                },
                legend: {
                    x: 'right',
                    data: ["DPU"]
                },
                toolbox: {
                    show: !0,
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    feature: {
                        magicType: {
                            show: !0,
                            title: {
                                line: "Line",
                                bar: "Bar",
                                stack: "Stack",
                                tiled: "Tiled"
                            },
                            type: ["line", "bar", "stack", "tiled"]
                        },
                        dataZoom : {
                            show: true,
                            title: {
                                zoom: "Zoom In",
                                back: "Zoom Out"
                            },
                        },
                        restore: {
                            show: !0,
                            title: "Restore"
                        },
                        saveAsImage: {
                            show: !0,
                            title: "Save Image"
                        }
                    }
                },
                calculable: !1,
                // dataZoom : {
                //     show : true,
                //     realtime : true,
                //     start : 0,
                //     end : 100
                // },
                xAxis: [{
                    type: "category",
                    data: data.date_list
                }],
                yAxis: [{
                    type: "value"
                }],
                series: [{
                    name: "DPU",
                    type: "line",
                    smooth: !0,
                    // itemStyle: {
                    //     normal: {
                    //         areaStyle: {
                    //             type: "default"
                    //         }
                    //     }
                    // },
                    markPoint: {
                        data: data.mark_data
                    },
                    data: data.dpu
                // }, {
                //     name: "Pre-order",
                //     type: "line",
                //     smooth: !0,
                //     itemStyle: {
                //         normal: {
                //             areaStyle: {
                //                 type: "default"
                //             }
                //         }
                //     },
                //     data: [30, 182, 434, 791, 390, 30, 10]
                // }, {
                //     name: "Intent",
                //     type: "line",
                //     smooth: !0,
                //     itemStyle: {
                //         normal: {
                //             areaStyle: {
                //                 type: "default"
                //             }
                //         }
                //     },
                //     data: [1320, 1132, 601, 234, 120, 90, 20]
                }]
            })
        }
}
}