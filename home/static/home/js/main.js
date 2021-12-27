window.onload = function () {
  const renderContainer = document.getElementById("render-container");
  const form = document.getElementById("search-form");

  const csrf = document.getElementsByName("csrfmiddlewaretoken");
  // const progressBar = document.getElementsByClassName("progress-bar");

  // Buttons
  const textForm = document.getElementById("text-form");
  const liveForm = document.getElementById("live-form");
  const uploadedForm = document.getElementById("upload-form");
  const details = document.getElementById("details");

  const text = document.getElementById("id_text");
  const liveTweet = document.getElementById("id_live_tweet");
  const fileInput = document.getElementById("id_file_name");
  console.log(fileInput);

  const alertBox = document.getElementById("alert-box");
  const progressBar = document.getElementById("progress-bar");

  MA = MA_window = MA_polarity = "";

  // For FormData and Graphical Results
  const resultHandler = (text) => {
    if (text == "Negative") {
      emoji_image = `<img src="../../static/home/images/angry2.png" alt="angry face emoji" /><p>${text}</p>`;
    } else if (text == "Positive") {
      emoji_image = `<img src="../../static/home/images/good2.png" alt="angry face emoji" /><p>${text}</p>`;
    } else {
      emoji_image = `<img src="../../static/home/images/neutral2.png" alt="angry face emoji" /><p>${text}</p>`;
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
      height: "12rem",
      opacity: "1",
      padding: "10px",
      transition: "2s",
    });

    $("#result-box").css({
      height: "10rem",
      opacity: "1",
    });
  };

  const pieChartHandler = (dataArray) => {
    dataArray = dataArray.map((num) => Math.round(num * 100));
    renderContainer.innerHTML += `
    <div class="chart">
         <canvas id="pie-chart" aria-label="Sentiment of Tweet Entered" role="img"></canvas>
    </div>`;
    // <div class="details-cross"></div>
    $(".chart").css({
      opacity: "1",
    });
    // Pie CHart
    const ctx = document.getElementById("pie-chart").getContext("2d");
    const pieChart = new Chart(ctx, {
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
      // plugins: [ChartDataLabels],
      options: {
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

    setTimeout(function (chart = pieChart) {
      chart.options.animation.delay = 0;
      chart.update();
      console.log("pie update triggered");
    }, 3500);
  };

  const lineChartHandler = (MA, MA_window, MA_polarity, MA_timestamps) => {
    renderContainer.innerHTML += `
    <div class="line-chart">
         <canvas id="line-chart" aria-label="${MA_window} Tweet Sentiment Moving Average" role="img"></canvas>
    </div>`;
    $(".line-chart").css({
      opacity: "1",
    });
    // Line CHart

    const lctx = document.getElementById("line-chart").getContext("2d");

    data = MA_polarity;
    data2 = MA;
    // Animation
    // const totalDuration = 5000;
    // const delayBetweenPoints = totalDuration / data.length;
    // const previousY = (lctx) =>
    //   lctx.index === 0
    //     ? lctx.chart.scales.y.getPixelForValue(100)
    //     : lctx.chart
    //         .getDatasetMeta(lctx.datasetIndex)
    //         .data[lctx.index - 1].getProps(["y"], true).y;
    // const animation = {
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
    const lineChart = new Chart(lctx, {
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
        fill: false,
        interaction: {
          intersect: false,
        },
        radius: 0,
        responsive: true,
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

    setTimeout(function (chart = lineChart) {
      chart.options.animation.delay = 0;
      chart.update();
    }, 3500);
  };

  // details.addEventListener("click", (event) => {});

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

  function spinnerToggle() {
    if ($("#spinner-box").css("opacity") == 0) {
      $("#spinner-box").css({
        height: "fit-content",
        opacity: "1",
        transition: "2s",
      });
      $("#spinner-box").html(
        `<img src="../../static/home/images/Dual Ring-1s-50px.svg" alt="">`
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

  textForm.addEventListener("submit", (e) => {
    spinnerToggle();
    e.preventDefault();

    const formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf[0].value);

    console.log(text);
    console.log(text.value);
    formdata.append("text", text.value);

    // For Form
    $.ajax({
      type: "POST",
      url: "",
      data: formdata,
      success: function (response) {
        console.log(response);
        spinnerToggle();
        resultHandler(response.sentiment);
        pieChartHandler(response.dataArray);
        pointer(response.polarity);
      },
      error: function () {
        console.log(error);
      },
      cache: false,
      contentType: false,
      processData: false,
    });
  });

  liveForm.addEventListener("submit", (e) => {
    spinnerToggle();
    e.preventDefault();

    const formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf[0].value);

    console.log(liveTweet);
    console.log(liveTweet.value);
    formdata.append("live_tweet", liveTweet.value);

    // For Form
    $.ajax({
      type: "POST",
      url: "",
      data: formdata,
      success: function (response) {
        console.log(response);
        spinnerToggle();
        resultHandler(response.sentiment);
        pieChartHandler(response.dataArray);
        lineChartHandler(
          response.MA,
          response.MA_window,
          response.MA_polarity,
          response.MA_timestamps
        );
        pointer(response.polarity);
        // MA = response.MA;
        // MA_window = response.MA_window;
        // MA_polarity = response.MA_polarity;
      },
      error: function () {
        console.log(error);
      },
      cache: false,
      contentType: false,
      processData: false,
    });
  });

  uploadedForm.addEventListener("submit", function (e) {
    spinnerToggle();
    e.preventDefault();

    const file_data = fileInput.files[0];
    console.log(file_data);

    const formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf[0].value);
    formdata.append("file_name", fileInput.files[0]);

    $.ajax({
      type: "POST",
      url: uploadedForm.action,
      enctype: "multipart/formdata",
      data: formdata,
      beforeSend: function () {},
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
        console.log(response);
        spinnerToggle();
        // console.log("spinner off");
        resultHandler(response.sentiment);
        pieChartHandler(response.dataArray);
        pointer(response.polarity);
        // spinnerToggle();
        // console.log("spinner off");
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
  //     `<img src="../../static/home/images/Dual Ring-1s-50px.svg" alt="">`
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
