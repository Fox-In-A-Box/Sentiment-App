window.onload = function () {
  // Divs
  const renderContainer = document.getElementById("render-container");
  // const form = document.getElementById("search-form"); //old form method

  // Csrf token from form
  const csrf = document.getElementsByName("csrfmiddlewaretoken").value;
  // const progressBar = document.getElementsByClassName("progress-bar");

  // Buttons
  const textForm = document.getElementById("text-form");
  // const textForm = document.getElementById("search-form"); //old form method
  const liveForm = document.getElementById("live-form");
  const uploadedForm = document.getElementById("upload-form");

  // Form Inputs
  // const text = document.getElementById("id_text"); //old form method
  const text = document.querySelector("input[name=text]");
  const liveTweet = document.querySelector("input[name=live_tweet]");
  const fileInput = document.querySelector("input[name=file_name]");
  // console.log(fileInput);

  // Other UI
  const alertBox = document.getElementById("alert-box");
  const progressBar = document.getElementById("progress-bar");

  // Moving Average Values for Line Chart
  // MA = MA_window = MA_polarity = "";

  // Display Results and Pie Chart Graph in render-conatiner div
  const resultHandler = (sentiment) => {
    if (sentiment == "Negative") {
      emoji_image = `<img src="../../static/./images/angry2.png" alt="angry face emoji" /><p>${sentiment}</p>`;
    } else if (sentiment == "Positive") {
      emoji_image = `<img src="../../static/./images/good2.png" alt="angry face emoji" /><p>${sentiment}</p>`;
    } else {
      emoji_image = `<img src="../../static/./images/neutral2.png" alt="angry face emoji" /><p>${sentiment}</p>`;
    }
    renderContainer.innerHTML = `
    <div id="result-box">
      <div class="polarity-bar">
          <div id="outer-pointer"></div>
          <svg id="svg1">
            <circle class="load" id="circle1" cx="64" cy="64" r="54" stroke-width="19.6"/>
            <circle class="load" id="circle2" cx="64" cy="64" r="54" stroke-width="19.8"/>
            <circle class="load" id="circle3" cx="64" cy="64" r="54" stroke-width="20"/>
          </svg>
      </div>
      <div class="emoji-container">
          ${emoji_image}
      </div>
    </div>`;

    $("#render-container").css({
      height: "11.5rem",
      width: "24.5rem",
      opacity: "1",
      padding: "10px",
      transition: "2s",
    });

    $("#result-box").css({
      height: "10rem",
      opacity: "1",
    });
  };

  // Pie Chart Generator Function
  const pieChartHandler = (dataArray) => {
    dataArray = dataArray.map((num) => Math.round(num * 100));
    renderContainer.innerHTML += `
    <div class="chart">
         <canvas id="pie-chart" aria-label="Sentiment of Tweet Entered" role="img"></canvas>
    </div>`;
    $(".chart").css({
      opacity: "1",
    });

    // Create Pie Chart
    var ctx = document.getElementById("pie-chart").getContext("2d");
    pieChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [
          {
            label: "Sentiment of Tweet Entered",
            data: dataArray,
            backgroundColor: ["#b3e59f", "#ffe07d", "#da387d"], //green #b3e59f, yellow #ffe07d, red #da387d
            hoverOffset: 4,
            normalized: true,
          },
        ],
      },
      // plugins: [ChartDataLabels], // Add datalabels to pie chart
      options: {
        layout: {
          padding: {
            left: 2, //set that fits the best
          },
        },
        animation: {
          duration: 1300,
          easing: "easeOutCubic",
          delay: 2000,
        },
        plugins: {
          // title: {
          //   display: true,
          //   position: "bottom",
          //   text: "Sentiment of Each Word",
          //   font: {
          //     family: "'Poppins', sans-serif",
          //   },
          // },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.label + ": " + context.parsed + "%";
              },
            },
          },
          legend: {
            position: "right",
            labels: {
              boxWidth: 10,
              boxHeight: 10,
              textAlign: "left",
              font: {
                family: "'Poppins', sans-serif",
              },
            },
          },
          // Uncomment for datalabels
          // datalabels: {
          //   formatter: (value) => {
          //     if (value > 0) {
          //       return value + "%";
          //     } else {
          //       return "";
          //     }
          //   },
          // },
        },
      },
    });

    // Resets animation delay on pie chart so tooltips animations arent delayed when hovering over the chart
    setTimeout(function (chart = pieChart) {
      chart.options.animation.delay = 0;
      chart.update();
      console.log("pie update triggered");
    }, 3500);
  };

  // Line and Pie Chart Generator Function
  const linePieChartHandler = (
    dataArray,
    MA,
    MA_window,
    MA_polarity,
    MA_timestamps
  ) => {
    dataArray = dataArray.map((num) => Math.round(num * 100));
    // renderContainer.innerHTML += `
    // <div class="chart">
    //      <canvas id="pie-chart" aria-label="Sentiment of Tweet Entered" role="img"></canvas>
    // </div>
    // <div class="line-chart">
    //      <canvas id="line-chart" aria-label="${MA_window} Tweet Sentiment Moving Average" role="img"></canvas>
    // </div>
    // <p id="wordcloud-title">Word Cloud</p>
    // <div id="wordcloud">
    //     <img src="../../static/images/wordcloud.png" alt="wordcloud">
    // </div>`;
    renderContainer.innerHTML += `
    <div class="chart">
         <canvas id="pie-chart" aria-label="Sentiment of Tweet Entered" role="img"></canvas>
    </div>
    <div class="line-chart">
         <canvas id="line-chart" aria-label="${MA_window} Tweet Sentiment Moving Average" role="img"></canvas>
    </div>
    <p id="wordcloud-title">Word Cloud</p>
    <div id="wordcloud">
      <div class="wordcloud-image">
        <img src="../../static/images/wordcloud.png" alt="wordcloud">
      </div>
    </div>`;

    $(".chart").css({
      opacity: "1",
    });
    $(".line-chart").css({
      opacity: "1",
    });

    var ctx = document.getElementById("pie-chart").getContext("2d");
    pieChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [
          {
            label: "Sentiment of Tweet Entered",
            data: dataArray,
            backgroundColor: ["#b3e59f", "#ffe07d", "#da387d"], //green #b3e59f, yellow #ffe07d, red #da387d
            hoverOffset: 4,
            normalized: true,
          },
        ],
      },
      // plugins: [ChartDataLabels], // Add datalabels to pie chart
      options: {
        layout: {
          padding: {
            left: 2, //set that fits the best
          },
        },
        animation: {
          duration: 1300,
          easing: "easeOutCubic",
          delay: 2000,
        },
        plugins: {
          // title: {
          //   display: true,
          //   position: "bottom",
          //   text: "Sentiment of Each Word",
          //   font: {
          //     family: "'Poppins', sans-serif",
          //   },
          // },
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.label + ": " + context.parsed + "%";
              },
            },
          },
          legend: {
            position: "right",
            labels: {
              boxWidth: 10,
              boxHeight: 10,
              textAlign: "left",
              font: {
                family: "'Poppins', sans-serif",
              },
            },
          },
          // Uncomment for datalabels
          // datalabels: {
          //   formatter: (value) => {
          //     if (value > 0) {
          //       return value + "%";
          //     } else {
          //       return "";
          //     }
          //   },
          // },
        },
      },
    });

    // Create Line Chart
    var lctx = document.getElementById("line-chart").getContext("2d");

    data = MA_polarity;
    data2 = MA;

    // var totalDuration = 10000;
    // var delayBetweenPoints = totalDuration / data.length;
    // var previousY = (lctx) =>
    //   lctx.index === 0
    //     ? lctx.chart.scales.y.getPixelForValue(100)
    //     : lctx.chart
    //         .getDatasetMeta(lctx.datasetIndex)
    //         .data[lctx.index - 1].getProps(["y"], true).y;
    // var animation = {
    //   x: {
    //     type: "number",
    //     easing: "linear",
    //     duration: delayBetweenPoints,
    //     from: NaN, // the point is initially skipped
    //     delay(lctx) {
    //       if (lctx.type !== "data" || lctx.xStarted) {
    //         return 0;
    //       }
    //       lctx.xStarted = true;
    //       return lctx.index * delayBetweenPoints;
    //     },
    //   },
    //   y: {
    //     type: "number",
    //     easing: "linear",
    //     duration: delayBetweenPoints,
    //     from: previousY,
    //     delay(lctx) {
    //       if (lctx.type !== "data" || lctx.yStarted) {
    //         return 0;
    //       }
    //       lctx.yStarted = true;
    //       return lctx.index * delayBetweenPoints;
    //     },
    //   },
    // };

    // Chart
    lineChart = new Chart(lctx, {
      type: "line",
      data: {
        labels: MA_timestamps,
        datasets: [
          {
            label: "Moving Average",
            data: data2,
            borderWidth: 2,
            borderColor: "rgb(54, 162, 235)",
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            tension: 0.4,
          },
          {
            label: "Polarity",
            data: data,
            borderWidth: 1.5,
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      },
      options: {
        // animation,
        animation: {
          duration: 1300,
          easing: "easeOutCubic",
          delay: 2000,
        },
        fill: false,
        interaction: {
          intersect: false,
        },
        radius: 0,
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            title: {
              display: true,
              text: `${MA_window} Tweet Sentiment Moving Average`,
              font: {
                family: "'Poppins', sans-serif",
              },
            },
            labels: {
              boxWidth: 10,
              boxHeight: 10,
              font: {
                family: "'Poppins', sans-serif",
              },
            },
          },
        },
        scales: {
          x: {
            ticks: {
              // font: {
              //   size: 5,
              // },
              callback: () => "",
            },
          },
        },
      },
    });

    setTimeout(function (chart = pieChart, chart2 = lineChart) {
      chart.options.animation.delay = 0;
      chart.update();
      chart2.options.animation.delay = 0;
      chart2.update();
    }, 3500);
  };

  // Plus Button Controller
  var expand = false;
  $(document).on("click", "#details", function () {
    var chart = Chart.getChart("line-chart");
    if (!expand) {
      $("#render-container").css({
        height: "80rem",
        width: "100%",
      });

      // document.getElementById("render-container").animate(
      //   [
      //     // keyframes
      //     { height: "11.5rem", width: "24.5rem", offset: 0 },
      //     { height: "11.5rem", width: "100%", offset: 0.5 },
      //     { height: "39rem", width: "100%", offset: 1 },
      //   ],
      //   {
      //     // timing options
      //     duration: 2000,
      //     easing: "ease-in-out",
      //     fill: "both",
      //   }
      // );
      chart.options.transitions = false;
      expand = true;
      console.log("expanded");
      setTimeout(function () {
        var chart = Chart.getChart("line-chart");
        chart.options.transitions = true;
      }, 2000);
    } else {
      $("#render-container").css({
        height: "11.5rem",
        width: "24.5rem",
      });
      // document.getElementById("render-container").animate(
      //   [
      //     // keyframes
      //     { height: "39rem", width: "100%", offset: 0 },
      //     { height: "11.5rem", width: "100%", offset: 0.5 },
      //     { height: "11.5rem", width: "24.5rem", offset: 1 },
      //   ],
      //   {
      //     // timing options
      //     duration: 2000,
      //     easing: "ease-in-out",
      //     fill: "both",
      //   }
      // );
      chart.options.transitions = false;
      expand = false;
      console.log("shrink");
      setTimeout(function () {
        var chart = Chart.getChart("line-chart");
        chart.options.transitions = true;
      }, 2000);
    }
  });

  // Moving Pointer on Sentiment Scale
  const pointer = (polarity) => {
    percent = 318 + ((polarity + 1) / 2) * 179;
    if (percent >= 318) {
      percent -= 360;
    }
    console.log(percent);

    document.getElementById("outer-pointer").animate(
      [
        // keyframes
        { transform: "rotate(-42deg)", opacity: 0, offset: 0 },
        {
          transform: "rotate(" + (percent + 10) + "deg)",
          opacity: 1,
          offset: 0.65,
        },
        { transform: "rotate(" + percent + "deg)", opacity: 1, offset: 1 },
      ],
      {
        // timing options
        duration: 2000,
        easing: "ease-in-out",
        delay: 2000,
        fill: "both",
      }
    );
  };

  // Spinner loading animation
  function spinnerToggle() {
    if ($("#spinner-box").css("opacity") == 0) {
      $("#spinner-box").css({
        height: "fit-content",
        opacity: "1",
        transition: "2s",
      });
      $("#spinner-box").html(
        `<img src="../../static/images/Dual Ring-1s-50px.svg" alt="">`
      );
    } else {
      $("#spinner-box").css({
        height: "0rem",
        opacity: "0",
        transition: "0~s",
      });
      $("#spinner-box").html(``);
    }
  }

  // Toggle Mask View and Box View for Word Cloud
  var mask = false;
  $(document).on("click", "#change-image-button", function () {
    if (!mask) {
      $("#change-image-box").html(`
          <button class="common-btn change-image-button" id="change-image-button">
            Mask View
          </button>
      `);
      $(".wordcloud-image").html(`
          <img src="../../static/images/wordcloud_mask.png" alt="wordcloud">
      `);
      $(".wordcloud-image").css({
        width: "100%",
        height: "40rem",
      });
      $("#render-container").css({
        height: "92.5rem",
      });

      mask = true;
    } else {
      $("#change-image-box").html(`
      <button class="common-btn change-image-button" id="change-image-button">
      Box View
      </button>
      `);
      $(".wordcloud-image").html(`
      <img src="../../static/images/wordcloud.png" alt="wordcloud">
      `);
      $(".wordcloud-image").css({
        width: "100%",
        height: "fit-content",
      });
      $("#render-container").css({
        height: "78rem",
      });
      mask = false;
    }
  });

  const mostCommonWords = (word_frequency) => {
    console.log(word_frequency);
    console.log(typeof word_frequency);
    $("#wordcloud").append(`
    <div id="common-words-box">
      <h1>Most Common Words</h1>
      <div id="common-words">
      </div>
    </div>
    `);

    // <h1>Most Common Words</h1>
    // <p><span>1.</span> ${word_frequency[0]}</p>
    // <p><span>2.</span> ${word_frequency[1]}</p>
    // <p><span>3.</span> ${word_frequency[2]}</p>
    // <p><span>4.</span> ${word_frequency[3]}</p>
    // <p><span>5.</span> ${word_frequency[4]}</p>
    for (var i = 0; i < 5; i++) {
      $("#common-words").append(
        `<p><span>${i + 1}.</span> ${word_frequency[i][0]} - ${
          word_frequency[i][1]
        }</p>`
      );
    }
  };

  // What to do when Text form is submitted
  textForm.addEventListener("submit", (e) => {
    spinnerToggle();
    e.preventDefault();

    // For Form
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/api/type/",
      header: {
        "X-CSRFToken": csrf,
      },
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({ text: text.value }), // Send JSON POST Request data to Type API
      success: function (response) {
        // Get JSON Response data from Type API as "response"
        console.log(response);
        spinnerToggle();
        resultHandler(response.sentiment);
        pieChartHandler(response.dataArray);
        pointer(response.polarity);
      },
      error: function (error) {
        console.log(error);
      },
      cache: false,
    });
  });

  liveForm.addEventListener("submit", (e) => {
    expand = false;
    spinnerToggle();
    e.preventDefault();
    // For Form
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/api/live/",
      header: {
        "X-CSRFToken": csrf,
      },
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({ live_tweet: liveTweet.value }),
      success: function (response) {
        console.log(response);
        spinnerToggle();
        resultHandler(response.sentiment);
        // renderContainer.innerHTML += `
        // <div class="details-box"><i id="details" class="fas fa-plus"></i></div>
        // `;
        renderContainer.innerHTML += `
        <div class="details-box"><i id="details" class="fas fa-plus"></i></div>
        <div id="change-image-box">
          <button class="common-btn change-image-button" id="change-image-button">
            Mask View
          </button>
        </div>
        `;
        linePieChartHandler(
          response.dataArray,
          response.MA,
          response.MA_window,
          response.MA_polarity,
          response.MA_timestamps
        );
        pointer(response.polarity);
        mostCommonWords(response.word_frequency);
      },
      error: function (error) {
        console.log(error);
      },
      cache: false,
    });
  });

  uploadedForm.addEventListener("submit", function (e) {
    spinnerToggle();
    e.preventDefault();

    const file_data = fileInput.files[0];
    console.log(file_data);

    const data = new FormData(this);
    // formdata.append("csrfmiddlewaretoken", csrf[0].value);
    // formdata.append("file_name", fileInput.files[0]);

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/api/csv/",
      enctype: "multipart/formdata",
      data: data,
      // beforeSend: function () {},
      // For Loading File Progress Bar
      xhr: function () {
        const xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", (e) => {
          if (e.lengthComputable) {
            const loadpercent = (e.loaded / e.total) * 100;
            console.log(loadpercent);
          }
        });
        return xhr;
      },
      success: function (response) {
        console.log("success!");
        spinnerToggle();
        resultHandler(response.sentiment);
        pieChartHandler(response.dataArray);
        pointer(response.polarity);
      },
      error: function () {
        console.log(error);
        spinnerToggle();
        resultHandler("Error");
      },
      cache: false,
      contentType: false,
      processData: false,
    });
  });

  // Upload Form Test Type3

  // form.addEventListener("submit", function (e) {
  //   $("#spinner-box").css({
  //     height: "fit-content",
  //     opacity: "1",
  //     transition: "2s",
  //   });
  //   $("#spinner-box").html(
  //     `<img src="../../static/./images/Dual Ring-1s-50px.svg" alt="">`
  //   );
  //   console.log("spinner on");

  //   e.preventDefault();

  //   const file_data = fileInput.files[0];
  //   console.log(file_data);

  //   const formdata = new FormData();
  //   formdata.append("csrfmiddlewaretoken", csrf[0].value);
  //   formdata.append("file_name", fileInput.files[0]);

  //   $.ajax({
  //     type: "POST",
  //     url: form.action,
  //     enctype: "multipart/formdata",
  //     data: formdata,
  //     beforeSend: function () {},
  //     xhr: function () {
  //       const xhr = new window.XMLHttpRequest();
  //       xhr.upload.addEventListener("progress", (e) => {
  //         if (e.lengthComputable) {
  //           const loadpercent = (e.loaded / e.total) * 100;
  //           console.log(loadpercent);
  //         }
  //       });
  //       return xhr;
  //     },
  //     success: function (response) {
  //       console.log(response);
  //       spinnerToggle();
  //       console.log("spinner off");
  //       resultHandler(response.sentiment);
  //       pieChartHandler(response.dataArray);
  //       pointer(response.polarity);
  //       // spinnerToggle();
  //       // console.log("spinner off");
  //     },
  //     error: function () {
  //       console.log(error);
  //     },
  //     cache: false,
  //     contentType: false,
  //     processData: false,
  //   });
  // });
  //   fetch("")
  //     .then(function (response) {
  //       return response.json();
  //     })
  //     .then(function (response) {
  //       console.log(response);
  //       resultHandler(response.sentiment);
  //       pieChartHandler(response.dataArray);
  //       pointer(response.polarity);
  //     });
  // });

  // console.log(form);
};
