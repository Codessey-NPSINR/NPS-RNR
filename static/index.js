function addressAutocomplete(containerElement, callback, options) {
  const MIN_ADDRESS_LENGTH = 3;
  const DEBOUNCE_DELAY = 300;

  // Section to kinda store everything
  const inputContainerElement = document.createElement("div");
  inputContainerElement.setAttribute("class", "input-container");
  containerElement.appendChild(inputContainerElement);

  const inputElement = document.createElement("input");
  inputElement.setAttribute("type", "text");
  inputElement.setAttribute("placeholder", options.placeholder);
  inputContainerElement.appendChild(inputElement);

  const clearButton = document.createElement("div");
  clearButton.classList.add("clear-button");
  addIcon(clearButton);
  clearButton.addEventListener("click", (e) => {
    e.stopPropagation();
    inputElement.value = "";
    callback(null);
    clearButton.classList.remove("visible");
    closeDropDownList();
  });
  inputContainerElement.appendChild(clearButton);

  // Timeout to make sure doesnt run too much and crash
  let currentTimeout;

  let currentPromiseReject;

  // User inputed smtg
  inputElement.addEventListener("input", function (e) {
    const currentValue = this.value;

    closeDropDownList();
    if (currentTimeout) {
      clearTimeout(currentTimeout);
    }
    if (currentPromiseReject) {
      currentPromiseReject({
        canceled: true,
      });
    }

    if (!currentValue) {
      clearButton.classList.remove("visible");
    }
    clearButton.classList.add("visible");

    if (!currentValue || currentValue.length < MIN_ADDRESS_LENGTH) {
      return false;
    }

    //  Call API thingy with a slight delay
    currentTimeout = setTimeout(() => {
      currentTimeout = null;

      /* Sending geocoding request */
      const promise = new Promise((resolve, reject) => {
        currentPromiseReject = reject;
        const apiKey = "eda87a4eea6b46509093c861f945e1e8";

        var url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(
          currentValue
        )}&format=json&limit=7&type=amenity&apiKey=${apiKey}`;

        fetch(url).then((response) => {
          currentPromiseReject = null;

          if (response.ok) {
            response.json().then((data) => resolve(data));
          } else {
            response.json().then((data) => reject(data));
          }
        });
      });

      promise.then(
        (data) => {
          // get the address suggestions thingy
          currentItems = data.results;

          const autocompleteItemsElement = document.createElement("div");
          autocompleteItemsElement.setAttribute(
            "class",
            "autocomplete-items"
          );
          inputContainerElement.appendChild(autocompleteItemsElement);

          /* For each result, make div and format */
          data.results.forEach((result, index) => {
            const itemElement = document.createElement("div");
            itemElement.innerHTML = result.formatted;
            autocompleteItemsElement.appendChild(itemElement);

            //   Changing the value of the inital input thing
            itemElement.addEventListener("click", function (e) {
              inputElement.value = currentItems[index].formatted;
              callback(currentItems[index]);
              closeDropDownList();
            });
          });
        },
        //   Idk if any error
        (err) => {
          if (!err.canceled) {
            console.log(err);
          }
        }
      );
    }, DEBOUNCE_DELAY);
  });

  function closeDropDownList() {
    const autocompleteItemsElement = inputContainerElement.querySelector(
      ".autocomplete-items"
    );
    if (autocompleteItemsElement) {
      inputContainerElement.removeChild(autocompleteItemsElement);
    }

    focusedItemIndex = -1;
  }

  function addIcon(buttonElement) {
    const svgElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "svg"
    );
    svgElement.setAttribute("viewBox", "0 0 24 24");
    svgElement.setAttribute("height", "24");

    const iconElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "path"
    );
    iconElement.setAttribute(
      "d",
      "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
    );
    iconElement.setAttribute("fill", "currentColor");
    svgElement.appendChild(iconElement);
    buttonElement.appendChild(svgElement);
  }

  /* Close dropdown when document clicked.  */
  document.addEventListener("click", function (e) {
    if (e.target !== inputElement) {
      closeDropDownList();
    } else if (!containerElement.querySelector(".autocomplete-items")) {
      // open dropdown list again
      var event = document.createEvent("Event");
      event.initEvent("input", true, true);
      inputElement.dispatchEvent(event);
    }
  });
}

addressAutocomplete(
  document.getElementById("autocomplete-container"),
  (data) => {
    console.log("Selected option: ");
    console.log(data);
  },
  {
    placeholder: "Enter an address here",
  }
);
