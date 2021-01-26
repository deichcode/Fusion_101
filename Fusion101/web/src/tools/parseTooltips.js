const parseTooltips = (text, tooltips) => {
    const openTag = '<span class="tooltip__trigger">'
    const closeTag = '</span>'
    let textWithTooltips = text;
    //replace markup by spans signaling that the word shows a tooltip and another span containing the tooltip
    tooltips.forEach(tooltip => {
        textWithTooltips = textWithTooltips.replace('___', openTag)
        const tooltipTriangle = '<span class="tooltip__triangle"> </span>'
        const tooltipContent = `<span class="tooltip__content">${tooltip}${tooltipTriangle}</span>`
        textWithTooltips = textWithTooltips.replace('___', tooltipContent +closeTag)
    })
    return textWithTooltips;
}

export default parseTooltips

