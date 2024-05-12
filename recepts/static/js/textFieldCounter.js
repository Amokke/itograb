const titleEl = document.querySelector('.recepe-form__title');
const titleCounter = titleEl.nextElementSibling;
const maxTitleLength = titleEl.maxLength;
const updateTitleCounter = (e) => {
  const len = e ? e.target.value.length : 0;
  titleCounter.textContent = `${len} / ${maxTitleLength}`;
}
updateTitleCounter();
titleEl.addEventListener('keyup', updateTitleCounter);
titleEl.addEventListener('keydown', updateTitleCounter);

const descriptionEl = document.querySelector('.recepe-form__description');
const descriptionCounter = descriptionEl.nextElementSibling;
const maxDescriptionLength = descriptionEl.maxLength;
const updateDescriptionCounter = (e) => {
  const len = e ? e.target.value.length : 0;
  descriptionCounter.textContent = `${len} / ${maxDescriptionLength}`;
}
updateDescriptionCounter();
descriptionEl.addEventListener('keyup', updateDescriptionCounter);
descriptionEl.addEventListener('keydown', updateDescriptionCounter);

const cookingStepsEl = document.querySelector('.recepe-form__cooking');
const cookingStepsCounter = cookingStepsEl.nextElementSibling;
const maxCookingStepsLength = cookingStepsEl.maxLength;
const updateCookingStepsCounter = (e) => {
  const len = e ? e.target.value.length : 0;
  cookingStepsCounter.textContent = `${len} / ${maxCookingStepsLength}`;
}
updateCookingStepsCounter();
cookingStepsEl.addEventListener('keyup', updateCookingStepsCounter);
cookingStepsEl.addEventListener('keydown', updateCookingStepsCounter);