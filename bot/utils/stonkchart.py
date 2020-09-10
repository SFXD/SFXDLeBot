import drawSvg as draw

class Chart:
    def __init__(self,
                 quotes, prev_close_quote,
                 chart_width=388,
                 chart_height=150,
                 chart_padding_top=10,
                 chart_padding_bottom=10,
                 chart_margin_top=3,
                 chart_margin_right=7,
                 chart_margin_bottom=0,
                 chart_margin_left=0,
                 font_size=14,
                 scale=1):
        # so many settings
        self.quotes = quotes
        self.prev_close_quote = prev_close_quote
        self.scale = scale
        self.chart_width = max(chart_width, len(quotes)-1) * scale
        self.chart_height = chart_height * scale
        self.chart_padding_top = chart_padding_top * scale
        self.chart_padding_bottom = chart_padding_bottom * scale
        self.chart_margin_top = 30 * scale
        self.chart_margin_right = 70 * scale
        self.chart_margin_bottom = 0 * scale
        self.chart_margin_left = 0 * scale
        self.font_size = font_size * scale

    def draw_chart(self):
        # Create a canvas for the chart
        canvas = draw.Drawing(
            self.chart_width + self.chart_margin_right + self.chart_margin_left,
            self.chart_height + self.chart_padding_top + self.chart_padding_bottom + self.chart_margin_top + self.chart_margin_bottom,
            displayInline=False)

        # create a chart using a polygon
        max_quote = self.prev_close_quote
        min_quote = self.prev_close_quote
        for quote in self.quotes:
            if quote is not None and quote > max_quote:
                max_quote = quote
            if quote is not None and quote < min_quote:
                min_quote = quote
        chart_ratio_y = (max_quote - min_quote) / self.chart_height
        step_x = self.scale
        start_x = self.chart_margin_left
        start_y = self.chart_margin_bottom
        offset_y = self.chart_margin_bottom + self.chart_padding_bottom
        end_x = start_x + (len(self.quotes)-1) * step_x
        end_y = start_y
        previous_close_y = ((self.prev_close_quote - min_quote) / chart_ratio_y) + offset_y
        last_y = ((self.quotes[len(self.quotes) - 1] - min_quote) / chart_ratio_y) + offset_y

        # create chart points
        points = []
        next_x = start_x - step_x
        next_y = None
        for idx in range(len(self.quotes)):
            point = self.quotes[idx]
            if point is not None:
                next_y = ((point - min_quote) / chart_ratio_y) + offset_y
            next_x += step_x
            points.append(next_x)
            points.append(next_y)
        points.append(end_x)
        points.append(end_y)

        # chart color
        chart_fill_rgb = "0,135,60"
        if (previous_close_y > last_y):
            chart_fill_rgb = "240,22,47"

        # draw chart with white background
        canvas.append(draw.Rectangle(
            start_x, self.chart_margin_bottom,
            self.chart_width, self.chart_height + self.chart_padding_top + self.chart_padding_bottom,
            fill="white"))
        canvas.append(draw.Lines(
            self.chart_margin_left, self.chart_margin_bottom, *points,
            close=True, fill="rgba({},0.5)".format(chart_fill_rgb), stroke="black"))

        # settings for creating tags and lines
        prev_close_value = round(self.prev_close_quote, 2)
        curr_close_value = round(self.quotes[len(self.quotes) - 1], 2)
        sig_figs = len(str(max(prev_close_value, curr_close_value)))
        self.width_tagrect = (self.font_size * (sig_figs - 1))
        self.height_tagrect = self.font_size + (self.font_size / 2)
        chart_boundary_x = start_x + self.chart_width

        # create tag for previous close
        prev_close_elements = self.create_tag_elements(prev_close_value, start_x, chart_boundary_x, previous_close_y, "grey")
        for el in prev_close_elements:
            canvas.append(el)

        # create tag for current close
        curr_close_elements = self.create_tag_elements(curr_close_value, start_x, chart_boundary_x, last_y, "rgb({})".format(chart_fill_rgb))
        for el in curr_close_elements:
            canvas.append(el)

        # convert svg to png
        png_bytes = canvas.rasterize().pngData
        return png_bytes

    def create_tag_elements(self, value, start_x, end_x, start_y, fill_color):
        # draw horizontal line across chart
        chart_line = draw.Line(start_x, start_y,
                               end_x, start_y,
                               stroke="black")
        # create tag polygon
        width_nubbin = self.font_size
        tag_rect = draw.Lines(end_x, start_y,
                              end_x + width_nubbin, start_y + self.height_tagrect / 2,
                              end_x + width_nubbin + self.width_tagrect, start_y + self.height_tagrect / 2,
                              end_x + width_nubbin + self.width_tagrect, start_y - self.height_tagrect / 2,
                              end_x + width_nubbin, start_y - self.height_tagrect / 2,
                              close=True, fill=fill_color)
        # create tag text
        tag_text = draw.Text(str(value), self.font_size,
                             end_x + width_nubbin, start_y - self.font_size * 0.3,
                             fill="white", font_family="monospace", font_weight="bold")
        return [chart_line, tag_rect, tag_text]
