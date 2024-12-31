export const toggleCollapsible = (event: Event): void => {
  const target = event.currentTarget as HTMLElement
  const plus = target.querySelector('.plus')
  const minus = target.querySelector('.minus')
  const content = target.nextElementSibling as HTMLElement

  plus?.classList.toggle('hidden')
  minus?.classList.toggle('hidden')

  if (target.classList.contains('rounded-full')) {
    target.classList.remove('rounded-full')
    target.classList.add('rounded-top')
  } else {
    target.classList.add('rounded-full')
    target.classList.remove('rounded-top')
  }

  if (content.style.maxHeight) {
    content.style.maxHeight = ''
  } else {
    content.style.maxHeight = `${content.scrollHeight}px`
  }
}
