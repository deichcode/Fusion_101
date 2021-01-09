const parseTooltips = (text, tooltips) => {
    const openTag = ' <span class="tooltip__trigger">'
    const closeTag = '</span> '
    let textWithTooltips = text;
    tooltips.forEach(tooltip => {
        textWithTooltips = textWithTooltips.replace(' __', openTag)
        const tooltipContent = `<span class="tooltip__content">${tooltip}</span>`
        textWithTooltips = textWithTooltips.replace('__ ', tooltipContent + closeTag)
    })
    return textWithTooltips;
}

export default parseTooltips

