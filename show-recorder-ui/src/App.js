import React, { useEffect, useState } from "react";
import axios from "axios";
import ReactAudioPlayer from "react-audio-player";
import { useTable, useSortBy, usePagination, useGlobalFilter } from "react-table";
import "./App.css";

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [diskUsage, setDiskUsage] = useState(null);
  const [playerError, setPlayerError] = useState(null);

  const closePlayer = () => {
    setCurrentFile(null);
    setPlayerError(null);
  };

  // Fetch the file list and disk usage from the API
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const [showsResponse, diskResponse] = await Promise.all([
          axios.get("/api/list_shows"),
          axios.get("/api/disk_usage"),
        ]);
        const data = showsResponse.data.shows;
        console.log("Fetched data:", data); // Log the fetched data
        setFiles(data);
        setDiskUsage(diskResponse.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  // Utility function to format file size
  const formatFileSize = (sizeInBytes) => {
    const sizeInMB = sizeInBytes / (1024 * 1024); // Convert bytes to MB
    return `${sizeInMB.toFixed(1)} MB`; // Format to 1 decimal place
  };

  // Pre-flight HEAD check before loading the audio player so errors are surfaced in the UI
  // rather than silently swallowed by the browser's audio element.
  const handlePreviewClick = async (fileName) => {
    setPlayerError(null);
    setCurrentFile(null);
    const url = `/api/preview/${encodeURIComponent(fileName)}`;
    try {
      const res = await fetch(url, { method: "HEAD" });
      if (!res.ok) {
        // Try to read the JSON error body from a GET (HEAD has no body)
        const bodyRes = await fetch(url);
        let message = `HTTP ${res.status}`;
        try {
          const json = await bodyRes.json();
          if (json.error) message = json.error;
        } catch (_) { }
        setPlayerError(message);
      } else {
        setCurrentFile(url);
      }
    } catch (err) {
      setPlayerError(`Network error: ${err.message}`);
    }
  };


  // Define table columns
  const columns = React.useMemo(
    () => [
      {
        id: "preview",
        Header: "Preview",
        accessor: "preview",
        disableSortBy: true,
        Cell: ({ row }) => {
          const fileName = row.original.filename;
          return (
            <button
              onClick={() => handlePreviewClick(fileName)}
              title="Preview"
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
              }}
            >
              🎵
            </button>
          );
        },
        getHeaderProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
      },
      {
        id: "name", // Unique ID for the column
        Header: "Name",
        accessor: "name",
      },
      {
        id: "start_date",
        Header: "Start Date",
        accessor: "start_date",
        sortType: (rowA, rowB) => rowA.original.start_timestamp - rowB.original.start_timestamp,
        getHeaderProps: () => ({
          style: { width: "150px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "150px", textAlign: "center" },
        }),
      },
      {
        id: "start_time",
        Header: "Start Time",
        accessor: "start_time",
        sortType: (rowA, rowB) => rowA.original.start_timestamp - rowB.original.start_timestamp,
        getHeaderProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
      },
      {
        id: "end_date",
        Header: "End Date",
        accessor: "end_date",
        sortType: (rowA, rowB) => rowA.original.end_timestamp - rowB.original.end_timestamp,
        getHeaderProps: () => ({
          style: { width: "150px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "150px", textAlign: "center" },
        }),
      },
      {
        id: "end_time",
        Header: "End Time",
        accessor: "end_time",
        sortType: (rowA, rowB) => rowA.original.end_timestamp - rowB.original.end_timestamp,
        getHeaderProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
      },
      {
        id: "size",
        Header: "Size",
        accessor: "size",
        Cell: ({ value }) => <span>{formatFileSize(value)}</span>,
        getHeaderProps: () => ({
          style: { width: "120px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "120px", textAlign: "center" },
        }),
      },
      {
        id: "chunk_number",
        Header: "Chunk Number",
        accessor: "chunk_number",
        disableSortBy: true,
        getHeaderProps: () => ({
          style: { width: "120px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "120px", textAlign: "center" },
        }),
      },
      {
        id: "download",
        Header: "Download",
        accessor: "download",
        disableSortBy: true,
        Cell: ({ row }) => {
          const fileName = row.original.filename;
          return (
            <a
              href={`/api/files/${encodeURIComponent(fileName)}`}
              download
              title="Download"
              style={{
                textDecoration: "none",
                fontSize: "1.2rem",
                color: "inherit",
              }}
            >
              📥
            </a>
          );
        },
        getHeaderProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
        getCellProps: () => ({
          style: { width: "100px", textAlign: "center" },
        }),
      },
    ],
    []
  );

  // Prepare data for the table
  const data = React.useMemo(
    () =>
      files.map((file) => ({
        name: file.name,
        start_date: file.start_date,
        start_time: file.start_time,
        start_timestamp: file.start_timestamp,
        end_date: file.end_date,
        end_time: file.end_time,
        end_timestamp: file.end_timestamp,
        filename: file.filename,
        size: file.size,
        chunk_number: file.chunk_number,
      })),
    [files]
  );

  // Use React Table hooks
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    page, // For pagination
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setGlobalFilter, // For search
    state: { pageIndex, globalFilter },
  } = useTable(
    {
      columns,
      data,
      initialState: {
        pageIndex: 0,
        pageSize: 15,
        hiddenColumns: ["start_timestamp", "end_timestamp", "filename"], // Hide these columns by default
        sortBy: [
          {
            id: "start_date", // Sort by the "Start Date" column
            desc: true, // Set the initial sort direction to descending
          },
        ],
      },
    }, useGlobalFilter, useSortBy, usePagination);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="App">
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>API error: {error}</p>}
      {!loading && !error && (
        <div>

          <h1>Recorded Shows</h1>

          <div className="search-disk-row">
            <div className="search-input-wrapper">
              <input
                value={globalFilter || ""}
                onChange={(e) => setGlobalFilter(e.target.value || undefined)}
                placeholder="Filter for..."
                className="search-input"
              />
              {globalFilter && (
                <button
                  className="search-clear-btn"
                  onClick={() => setGlobalFilter(undefined)}
                  title="Clear filter"
                >
                  &times;
                </button>
              )}
            </div>

            {diskUsage && (() => {
              const pct = diskUsage.percent_used;
              const color = pct <= 70 ? "#2a9d2a" : pct <= 93 ? "orange" : "red";
              const usedGB = (diskUsage.used / 1024 ** 3).toFixed(2);
              const totalGB = (diskUsage.total / 1024 ** 3).toFixed(2);
              return (
                <div className="disk-bar-wrapper" style={{ marginBottom: 0 }}>
                  <span className="disk-bar-label">
                    {usedGB} GB used of {totalGB} GB ({pct}% used)
                  </span>
                  <div className="disk-bar-track">
                    <div
                      className="disk-bar-fill"
                      style={{ width: `${pct}%`, backgroundColor: color }}
                    />
                  </div>
                </div>
              );
            })()}
          </div>

          <table {...getTableProps()} className="file-table">
            <thead>
              {headerGroups.map((headerGroup) => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map((column) => (
                    <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                      {column.render("Header")}
                      <span>
                        {column.isSorted
                          ? column.isSortedDesc
                            ? " 🔽"
                            : " 🔼"
                          : ""}
                      </span>
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {page.map((row) => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()}>
                    {row.cells.map((cell) => (
                      <td
                        {...cell.getCellProps({
                          className: `cell-${cell.column.id}`, // Add a class based on the column ID
                        })}
                      >
                        {cell.render("Cell")}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>

          {/* Audio Player */}
          {(currentFile || playerError) && (
            <div className="audio-player">
              <div className="audio-player-header">
                <h2>Preview Player</h2>
                <button
                  className="audio-player-close"
                  onClick={closePlayer}
                  aria-label="Close preview player"
                  title="Close preview player"
                >
                  Close
                </button>
              </div>
              {playerError ? (
                <p className="audio-player-error">
                  &#9888; Preview error: {playerError}
                </p>
              ) : (
                <>
                  <p className="audio-player-filename">
                    {decodeURIComponent(currentFile.split("/").pop())}
                  </p>
                  <ReactAudioPlayer
                    src={currentFile}
                    controls
                    autoPlay
                    style={{ width: "100%" }}
                    onError={() => setPlayerError("Playback error - the file may be unavailable or still recording.")}
                  />
                </>
              )}
            </div>
          )}

          {/* Pagination Controls */}
          <div className="pagination">
            <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
              {"<<"}
            </button>
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
              {"<"}
            </button>
            <span>
              Page {" "}
              <strong>
                {pageIndex + 1} of {pageOptions.length}
              </strong>{" "}
            </span>
            <button onClick={() => nextPage()} disabled={!canNextPage}>
              {">"}
            </button>
            <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
              {">>"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
