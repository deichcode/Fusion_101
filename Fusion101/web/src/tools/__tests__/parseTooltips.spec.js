import parseTooltips from "@/tools/parseTooltips";

describe('parseTooltips', function () {
    it('should not change text if no tooltip marker exists', () => {
        const text = "Text without tooltip";

        const result = parseTooltips(text, [""])

        expect(result).toBe(text)
    });

    it('should replace first ___ with trigger open tag', () => {
        const text = "Text ___with___ tooltip";

        const result = parseTooltips(text, [""])

        expect(result).toContain('<span class="tooltip__trigger">with')
    })

    it('should insert close tag after tooltip content', () => {
        const text = "Text ___with___ tooltip";

        const result = parseTooltips(text, [""])

        expect(result).toContain('</span></span> tooltip')
    })

    it('should insert tooltip content before trigger close tag', () => {
        const text = "Text ___with___ tooltip";
        const tooltipContent = "Tooltip content"

        const result = parseTooltips(text, [tooltipContent])

        expect(result).toContain(`with<span class="tooltip__content">${tooltipContent}</span></span>`)
    })

    it('should enter open span at start of text', function () {
        const text = "___Starts___ with tooltip";
        const tooltipContent = "Tooltip content"

        const result = parseTooltips(text, [tooltipContent])

        expect(result).toContain('<span class="tooltip__trigger">Start')
    });

    it('should enter open span at start of text', function () {
        const text = "Ends with ___tooltip___";
        const tooltipContent = "Tooltip content"

        const result = parseTooltips(text, [tooltipContent])

        expect(result).toContain('</span>')
    });

    it('should insert tooltips at multiple positions', () => {
        const text = "Text with ___first___ and ___second___ tooltip"
        const firstTooltipContent = "First tooltip"
        const secondTooltipContent = "Second tooltip"
        const tooltips = [firstTooltipContent, secondTooltipContent]

        const result = parseTooltips(text, tooltips)

        expect(result).toBe("" +
            "Text with " +
            `<span class="tooltip__trigger">first<span class="tooltip__content">${firstTooltipContent}</span></span>` +
            " and " +
            `<span class="tooltip__trigger">second<span class="tooltip__content">${secondTooltipContent}</span></span>` +
            " tooltip"

        )
    });

    it('should not throw an error if no markup for replace exists', () => {
        const text = "Text without markdown for tooltip"

        const result = parseTooltips(text, ["Tooltip"])

        expect(result).toBe(text)
    })

    it('should not throw an error if no tooltips are provided', () => {
        const text = "Text __without__ markdown for tooltip"

        const result = parseTooltips(text, [])

        expect(result).toBe(text)
    })
});