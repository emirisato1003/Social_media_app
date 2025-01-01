const input = document.querySelector('input[name="img_file"]')
const output = document.querySelector('output')
let imagesArray = []
// console.log(input, output)

input.addEventListener('change', () => {
    const file = input.files[0]
    imagesArray = [file]
    displayImages()
})

const displayImages = () => {
    output.innerHTML = ''
    imagesArray.forEach((image) => {
        const img = document.createElement('img')
        img.className = 'img-fluid mb-3 w-50'
        img.src = URL.createObjectURL(image)
        img.alt = image.name
        output.appendChild(img)
    })
}