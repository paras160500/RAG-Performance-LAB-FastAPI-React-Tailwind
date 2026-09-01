function RetrievalResults({
  data,
}) {
  if (!data) {
    return (
      <div className="empty-state">
        No search performed yet.
      </div>
    );
  }

  const results =
    data.results || [];

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Vector Index</th>
            <th>Similarity</th>
          </tr>
        </thead>

        <tbody>
          {results.map(
            (item, index) => (
              <tr
                key={`${item.index}-${index}`}
              >
                <td>
                  #{index + 1}
                </td>

                <td>
                  {item.index}
                </td>

                <td>
                  {Number(
                    item.similarity
                  ).toFixed(6)}
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
}


export default RetrievalResults;