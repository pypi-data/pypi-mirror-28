from visidata import *

globalCommand('M', 'vd.push(MeltedSheet(sheet))', 'open melted sheet (unpivot)')

melt_var_colname = 'Variable' # column name to use for the melted variable name
melt_value_colname = 'Value'  # column name to use for the melted value

# rowdef: (sourceRow, sourceCol)
class MeltedSheet(Sheet):
    "Perform 'melt', the reverse of 'pivot', on input sheet."
    rowtype = 'melted values'
    def __init__(self, sheet):
        super().__init__(sheet.name + '_melted', source=sheet)

    @async
    def reload(self):
        sheet = self.source
        self.columns = [SubrowColumn(c, 0) for c in sheet.keyCols]
        self.nKeys = sheet.nKeys
        self.columns.extend([Column(melt_var_colname, getter=lambda col,row: row[1].name),
                             Column(melt_value_colname, getter=lambda col,row: row[1].getValue(row[0]))])

        colsToMelt = [copy(c) for c in sheet.nonKeyVisibleCols]

        self.rows = []
        for r in Progress(self.source.rows):
            for c in colsToMelt:
                if c.getValue(r) is not None:
                    self.addRow((r, c))
