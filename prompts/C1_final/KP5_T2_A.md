请用课程数据算历史法VaR。文件是data/market_snapshot_v1.csv，取fund列的日收益，头寸100万元。画日损益的直方图，把95%一日历史VaR标成一条线，置信水平做成可调。VaR的数值也告诉我。

输出契约：把所有要求的输出存入名为 `result` 的字典，键名严格为：'hist_var_95_1d', 'figure_path'。 将图保存为文件，并把文件路径存入 result['figure_path']。
