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

  // Fetch the file list from the API
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get("/api/list_shows");
        const data = response.data.shows;
        console.log("Fetched data:", data); // Log the fetched data
        setFiles(data);
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
              onClick={() => setCurrentFile(`/api/files/${fileName}`)}
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
              href={`/api/files/${fileName}`}
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

        {/* Search/Filter Input */}
        <input
          value={globalFilter || ""}
          onChange={(e) => setGlobalFilter(e.target.value || undefined)} // Set undefined to reset the filter
          placeholder="Filter for..."
          style={{
            marginBottom: "10px",
            padding: "8px",
            width: "100%",
            maxWidth: "400px",
          }}
        />

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
        {currentFile && (
          <div className="audio-player">
            <h2>Now Playing</h2>
            <p style={{ marginTop: "10px", fontStyle: "italic" }}>
              {currentFile.split("/").pop()} {/* Extract the file name */}
            </p>
            <ReactAudioPlayer
              src={currentFile}
              controls
              autoPlay
              style={{ width: "100%" }}
            />
            
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
