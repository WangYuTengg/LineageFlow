import { useNavigate } from 'react-router-dom';

interface Repository {
  repo_name: string;
  description: string;
  bucket_url: string;
  default_branch: string;
  branches: string[];
  created_at: string | null;
}

interface TableRepositoriesProps {
  data: Repository[];
}

export default function TableRepositories({ data }: TableRepositoriesProps) {
  const navigate = useNavigate();

  const rows = data.map((repo) => {
    const createdAt = repo.created_at ? new Date(repo.created_at) : null;
    const createdAtStr = createdAt && !isNaN(createdAt.getTime()) ? createdAt.toISOString() : 'Invalid date';

    const handleClick = () => {
      navigate(`/repositories/${repo.repo_name}`);
    };

    return (
      <div key={repo.repo_name} className="border rounded-lg p-4 mb-4">
        <button
          onClick={handleClick}
          className="text-blue-400 hover:underline text-2xl font-semibold"
        >
          {repo.repo_name}
        </button>
        <div className="text-gray-500 mt-2">
          created at <span className="text-red-500">{createdAtStr}</span> (X hours ago)
        </div>
        <div className="text-gray-500 mt-2">
          default branch: <span className="text-red-500">{repo.default_branch}</span>, storage namespace: <span className="text-red-500">{repo.bucket_url}</span>
        </div>
      </div>
    );
  });

  return <div>{rows}</div>;
}
