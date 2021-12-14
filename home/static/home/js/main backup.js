window.onload = function () {
  const renderContainer = document.getElementById("render-container");
  const form = document.getElementById("search-form");

  const csrf = document.getElementsByName("csrfmiddlewaretoken");
  const text = document.getElementById("id_text");

  const resultHandler = (text) => {
    if (text == "Negative") {
      emoji_image = `<img src="../../static/home/images/angry2.png" alt="angry face emoji" /><p>${text}</p>`;
    } else if (text == "Positive") {
      emoji_image = `<img src="../../static/home/images/good2.png" alt="angry face emoji" /><p>${text}</p>`;
    } else {
      emoji_image = `<img src="../../static/home/images/neutral2.png" alt="angry face emoji" /><p>${text}</p>`;
    }
    renderContainer.innerHTML = `<div id="result-box"></div>`;

    setTimeout(function () {
      document.getElementById("result-box").innerHTML = `
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
      </div>`;
    }, 0);
    // Setting timeout offset so it will do this after the element has loaded
    setTimeout(function () {
      document.getElementById("result-box").animate(
        [
          // keyframes
          { height: "0rem", opacity: 0, offset: 0 },
          { height: "10rem", opacity: 1, offset: 1 },
        ],
        {
          // timing options
          duration: 1999,
          easing: "ease",
          fill: "both",
        }
      );
    }, 1);

    renderContainer.animate(
      [
        // keyframes
        {
          height: "0rem",
          width: "fit-content",
          opacity: 0,
          padding: "0px",
          offset: 0,
        },
        {
          height: "12rem",
          width: "fit-content",
          opacity: 1,
          padding: "10px",
          offset: 1,
        },
      ],
      {
        // timing options
        duration: 2000,
        easing: "ease",
        fill: "both",
      }
    );
  };

  const chartHandler = (dataArray) => {
    dataArray = dataArray.map((num) => Math.round(num * 100));
    renderContainer.innerHTML += `
    <div class="chart">
         <canvas id="pie-chart" aria-label="Sentiment of Tweet Entered" role="img"></canvas>
    </div>`;
    $(".chart").css({
      opacity: "1",
    });
    // Pie CHart
    const ctx = document.getElementById("pie-chart").getContext("2d");
    const myChart = new Chart(ctx, {
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

    setTimeout(function (chart = myChart) {
      chart.options.animation.delay = 0;
      chart.update();
    }, 3500);
  };

  const pointer = (polarity) => {
    percent = 318 + ((polarity + 1) / 2) * 179;
    if (percent >= 318) {
      percent -= 360;
    }
    console.log(percent);
    setTimeout(function () {
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
          delay: 1999,
          fill: "both",
        }
      );
    }, 1);
  };
  //   const loadElement = function () {
  //     if (!$("#circle1").hasClass("load")) {
  //       $("#circle1").addClass("load");
  //     }
  //     if (!$("#circle2").hasClass("load")) {
  //       $("#circle2").addClass("load");
  //     }
  //     if (!$("#circle3").hasClass("load")) {
  //       $("#circle3").addClass("load");
  //     }
  //   };

  // Pie CHart
  //   const chart = (dataArray) => {
  //     const ctx = document.getElementById("pie-chart");
  //     const myChart = new Chart(ctx, {
  //       type: "bar",
  //       data: {
  //         labels: ["Positive", "Neutral", "Negative"],
  //         datasets: [
  //           {
  //             label: "Sentiment of Tweet Entered",
  //             data: dataArray,
  //             backgroundColor: ["#b3e59f", "#ffe07d", "#da387d"], //green #b3e59f, yellow #ffe07d, red #da387d
  //             hoverOffset: 4,
  //             normalized: true,
  //           },
  //         ],
  //       },
  //       options: {
  //         scales: {
  //           y: {
  //             beginAtZero: true,
  //           },
  //         },
  //         // plugins: {
  //         //   deferred: {
  //         //     xOffset: "50%", // defer until 150px of the canvas width are inside the viewport
  //         //     yOffset: "50%", // defer until 50% of the canvas height are inside the viewport
  //         //     delay: 4000, // delay of 500 ms after the canvas is considered inside the viewport
  //         //   },
  //         // },
  //       },
  //     });
  //   };
  // AJAX
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", csrf[0].value);
    formdata.append("text", text.value);
    // For Form
    $.ajax({
      type: "POST",
      url: "",
      data: formdata,
      success: function (response) {
        console.log(response);
        resultHandler(response.sentiment);
        chartHandler(response.dataArray);
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

  console.log(form);
};
